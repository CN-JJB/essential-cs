#!/usr/bin/env python3
"""
labs/foundations/m17/trace_harness.py

Essential CS — Module M17 Worked-Trace Harness
Bounded State/Message/Failure Traces for Replication, Consensus & Consistency.

CORE BOUNDARY ENFORCEMENT:
- Strictly ZERO distributed service daemons.
- Strictly ZERO listening network sockets or external ports.
- Strictly ZERO multi-node background processes or Docker containers.
- Strictly NO full Raft or Paxos implementation.
- Nodes are logical worksheet / state-machine records.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


# ==============================================================================
# Trace Family 1: Replication Acknowledgment Semantics & Durability
# ==============================================================================

class AckPolicy(Enum):
    ASYNC = "ASYNC"                 # Course scenario: ack after leader-local modeled write
    SEMI_SYNC = "SEMI_SYNC"         # Course scenario: ack after a configured follower threshold
    SYNC_ALL = "SYNC_ALL"           # Course scenario: ack after every modeled replica confirms
    QUORUM_W = "QUORUM_W"           # Course scenario: ack after W modeled replicas confirm


class StorageDurability(Enum):
    # These are worksheet assumptions only. The harness performs no real fsync/disk test.
    VOLATILE_RAM = "VOLATILE_RAM"
    DURABLE_DISK = "DURABLE_DISK"


@dataclass
class ReplicaState:
    node_id: str
    is_leader: bool = False
    is_alive: bool = True
    reachable_from_leader: bool = True
    storage: StorageDurability = StorageDurability.DURABLE_DISK
    log: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ReplicationAckTrace:
    policy: AckPolicy
    cluster_size: int
    w_quorum: int
    replicas: Dict[str, ReplicaState]
    client_acked: bool = False
    ack_error: Optional[str] = None
    acknowledged_replicas: Set[str] = field(default_factory=set)
    replicas_at_client_ack: Set[str] = field(default_factory=set)
    required_follower_acks: int = 1

    @classmethod
    def simulate_write(
        cls,
        policy: AckPolicy,
        cluster_size: int,
        leader_id: str,
        unreachable_replicas: Set[str],
        crashed_after_write_leader: bool = False,
        w_quorum: int = 2,
        required_follower_acks: int = 1,
    ) -> "ReplicationAckTrace":
        """
        Simulate one bounded acknowledgment-point worksheet.

        "unreachable_replicas" means unreachable from the old leader during this
        modeled write step; it does NOT mean those replicas are dead forever.
        """
        if cluster_size < 1:
            raise ValueError("cluster_size must be positive")
        node_ids = [f"node_{i+1}" for i in range(cluster_size)]
        if leader_id not in node_ids:
            raise ValueError("leader_id must name a modeled replica")
        if not (1 <= w_quorum <= cluster_size):
            raise ValueError("w_quorum must be within the modeled cluster")
        if required_follower_acks < 0 or required_follower_acks > cluster_size - 1:
            raise ValueError("required_follower_acks is outside the modeled follower set")

        replicas = {
            nid: ReplicaState(
                node_id=nid,
                is_leader=(nid == leader_id),
                is_alive=True,
                reachable_from_leader=(nid == leader_id or nid not in unreachable_replicas),
            )
            for nid in node_ids
        }

        entry = {"key": "balance", "val": 100, "version": 1}
        replicas_with_entry: Set[str] = set()
        replicas_at_ack: Set[str] = set()

        leader = replicas[leader_id]
        leader.log.append(dict(entry))
        replicas_with_entry.add(leader_id)

        reachable_followers = [
            nid
            for nid in node_ids
            if nid != leader_id and replicas[nid].reachable_from_leader
        ]

        client_acked = False
        ack_error = None

        if policy == AckPolicy.ASYNC:
            # Ack point occurs before any follower replication in this scenario.
            client_acked = True
            replicas_at_ack = {leader_id}

        elif policy == AckPolicy.SEMI_SYNC:
            # "Semi-sync" is not a universal one-follower definition; this worksheet
            # uses a configurable follower threshold.
            selected = reachable_followers[:required_follower_acks]
            for nid in selected:
                replicas[nid].log.append(dict(entry))
                replicas_with_entry.add(nid)
            if len(selected) >= required_follower_acks:
                client_acked = True
                replicas_at_ack = set(replicas_with_entry)
            else:
                ack_error = "SEMI_SYNC_REPLICA_TIMEOUT"

        elif policy == AckPolicy.SYNC_ALL:
            for nid in reachable_followers:
                replicas[nid].log.append(dict(entry))
                replicas_with_entry.add(nid)
            if len(replicas_with_entry) == cluster_size:
                client_acked = True
                replicas_at_ack = set(replicas_with_entry)
            else:
                ack_error = "SYNC_ALL_TIMEOUT_FOLLOWER_UNREACHABLE"

        elif policy == AckPolicy.QUORUM_W:
            needed_followers = max(0, w_quorum - 1)
            selected = reachable_followers[:needed_followers]
            for nid in selected:
                replicas[nid].log.append(dict(entry))
                replicas_with_entry.add(nid)
            if len(replicas_with_entry) >= w_quorum:
                client_acked = True
                replicas_at_ack = set(replicas_with_entry)
            else:
                ack_error = "QUORUM_WRITE_UNSATISFIED"

        # Ambiguous outcome: the modeled leader crashes after the selected replication
        # step but before the client observes success. Remote state may still contain
        # the entry even though client_acked is false.
        if crashed_after_write_leader:
            leader.is_alive = False
            client_acked = False
            replicas_at_ack = set()
            ack_error = "CLIENT_TIMEOUT_LEADER_CRASHED_POST_REPLICATION"

        return cls(
            policy=policy,
            cluster_size=cluster_size,
            w_quorum=w_quorum,
            replicas=replicas,
            client_acked=client_acked,
            ack_error=ack_error,
            acknowledged_replicas=set(replicas_with_entry),
            replicas_at_client_ack=replicas_at_ack,
            required_follower_acks=required_follower_acks,
        )

    def evaluate_failover_loss(self, new_leader_id: str) -> Dict[str, Any]:
        """
        Evaluate whether the acknowledged write survives failover to a new leader.
        """
        new_leader = self.replicas.get(new_leader_id)
        if not new_leader:
            return {"valid_failover": False, "reason": "NEW_LEADER_DOES_NOT_EXIST"}

        has_entry = len(new_leader.log) > 0
        data_lost = self.client_acked and not has_entry

        return {
            "valid_failover": True,
            "new_leader": new_leader_id,
            "has_entry": has_entry,
            "data_lost": data_lost,
            "durability_verdict": "DATA_LOST_ON_FAILOVER" if data_lost else "SURVIVED_FAILOVER",
        }


# ==============================================================================
# Trace Family 2: Quorum Set-Intersection Validator & Counterexamples
# ==============================================================================

@dataclass
class QuorumValidator:
    """
    Validates quorum arithmetic and demonstrates why set overlap alone
    does NOT guarantee reading the latest value or linearizability.
    """
    cluster_size: int  # N
    write_quorum: int  # W
    read_quorum: int   # R

    def is_quorum_valid(self) -> bool:
        """
        Pigeonhole Principle check: W + R > N.
        Guarantees that any write quorum and read quorum must intersect
        in at least (W + R - N) >= 1 node.
        """
        return (self.write_quorum + self.read_quorum) > self.cluster_size

    def min_overlap_count(self) -> int:
        overlap = (self.write_quorum + self.read_quorum) - self.cluster_size
        return max(0, overlap)

    def evaluate_overlap(
        self,
        write_set: Set[str],
        read_set: Set[str],
    ) -> Dict[str, Any]:
        overlap_nodes = write_set.intersection(read_set)
        return {
            "write_set": sorted(list(write_set)),
            "read_set": sorted(list(read_set)),
            "overlap_nodes": sorted(list(overlap_nodes)),
            "has_overlap": len(overlap_nodes) >= 1,
            "overlap_size": len(overlap_nodes),
        }

    @staticmethod
    def demonstrate_counterexample_unversioned_stale_read() -> Dict[str, Any]:
        """
        COUNTEREXAMPLE 1: Overlap without versioning yields stale read.
        N=3, W=2, R=2.
        Write v2 completed on {N1, N2}. N3 still holds v1.
        Read quorum is {N2, N3}. Overlap is {N2}.
        If reader has no version tie-breaker or reads the first-arriving response,
        reader can return v1 from N3.
        PROVES: Overlap alone does NOT equal latest-value read!
        """
        replicas = {
            "N1": {"val": "v2", "version": 2},
            "N2": {"val": "v2", "version": 2},
            "N3": {"val": "v1", "version": 1},
        }
        read_set = {"N2", "N3"}
        read_values = [replicas[n] for n in read_set]

        # Stale read if client blindly takes first response or lacks version comparison
        blind_read_value = replicas["N3"]["val"]  # N3 responded first
        resolved_value = max(read_values, key=lambda x: x["version"])["val"]

        return {
            "scenario": "UNVERSIONED_READ_FROM_OVERLAP",
            "write_quorum": ["N1", "N2"],
            "read_quorum": ["N2", "N3"],
            "overlap": ["N2"],
            "blind_first_response_value": blind_read_value,
            "version_resolved_value": resolved_value,
            "stale_read_manifested": blind_read_value != "v2",
            "proof": "OVERLAP_ALONE_INSUFFICIENT_WITHOUT_VERSION_RULE",
        }

    @staticmethod
    def demonstrate_counterexample_ambiguous_partial_write() -> Dict[str, Any]:
        """
        COUNTEREXAMPLE 2: Incomplete/failed write causes non-linearizable history.
        N=3, W=2, R=2.
        Write v2 writes to N1 only, then crashes before N2 receives it.
        Write returned FAILURE/TIMEOUT to Client 1 (unacknowledged/ambiguous).
        Now Reader 1 reads {N1, N2} -> observes v2 on N1, returns v2.
        Later Reader 2 reads {N2, N3} -> neither has v2, returns v1!
        PROVES: A later read returned an older value than an earlier read.
        Overlap existed, but history violates real-time precedence (non-linearizable)
        unless read-repair / commit consensus is enforced.
        """
        replicas = {
            "N1": {"val": "v2", "version": 2},
            "N2": {"val": "v1", "version": 1},
            "N3": {"val": "v1", "version": 1},
        }
        # Reader 1 reads {N1, N2}
        r1_set = {"N1", "N2"}
        r1_val = max([replicas[n] for n in r1_set], key=lambda x: x["version"])["val"]

        # Reader 2 reads {N2, N3}
        r2_set = {"N2", "N3"}
        r2_val = max([replicas[n] for n in r2_set], key=lambda x: x["version"])["val"]

        return {
            "scenario": "AMBIGUOUS_PARTIAL_WRITE_COUNTEREXAMPLE",
            "partial_write_replicas": ["N1"],
            "reader_1_quorum": sorted(list(r1_set)),
            "reader_1_observed": r1_val,
            "reader_2_quorum": sorted(list(r2_set)),
            "reader_2_observed": r2_val,
            "linearizability_violated": (r1_val == "v2" and r2_val == "v1"),
            "proof": "OVERLAP_ALONE_DOES_NOT_GUARANTEE_LINEARIZABILITY",
        }

    @staticmethod
    def demonstrate_counterexample_concurrent_conflicting_writes() -> Dict[str, Any]:
        """
        COUNTEREXAMPLE 3: Concurrent conflicting writes under quorum overlap.
        N=3, W=2, R=2.
        Client A writes 'A' to WA={N1, N2}.
        Client B writes 'B' to WB={N2, N3}.
        Both quorums overlap at N2.
        At N1: holds 'A'.
        At N3: holds 'B'.
        At N2: whichever packet arrived last overwrote the other.
        Without a named version/order/conflict-resolution protocol, Reader {N1, N3}
        sees conflicting values and the set-overlap fact alone does not select a winner.
        """
        return {
            "scenario": "CONCURRENT_WRITES_WITHOUT_CONSENSUS",
            "client_A_quorum": ["N1", "N2"],
            "client_B_quorum": ["N2", "N3"],
            "overlap_node": "N2",
            "replica_states": {
                "N1": "A",
                "N2": "B (overwritten by B)",
                "N3": "B",
            },
            "disjoint_readers_anomaly": "Reader {N1, N2} sees B; Reader {N1} only sees A",
            "proof": "QUORUM_OVERLAP_CANNOT_RESOLVE_CONCURRENT_WRITE_ORDER_WITHOUT_A_NAMED_ORDER_CONFLICT_RULE",
        }


# ==============================================================================
# Trace Family 3: Bounded Raft Vote & Log Safety Worksheet
# ==============================================================================

@dataclass
class RaftLogEntry:
    index: int
    term: int
    command: str


@dataclass
class RaftNodeRecord:
    node_id: str
    current_term: int
    voted_for: Optional[str] = None
    log: List[RaftLogEntry] = field(default_factory=list)

    @property
    def last_log_index(self) -> int:
        return self.log[-1].index if self.log else 0

    @property
    def last_log_term(self) -> int:
        return self.log[-1].term if self.log else 0


class RaftTraceValidator:
    """
    Evaluates bounded Raft vote requests against the Log Up-To-Date rule
    and examines the boundary of Majority Overlap vs. Leader Completeness.
    """

    @staticmethod
    def is_candidate_log_up_to_date(
        cand_last_term: int,
        cand_last_index: int,
        voter_last_term: int,
        voter_last_index: int,
    ) -> bool:
        """
        Raft §5.4.1 Election Restriction:
        Candidate's log is at least as up-to-date as voter's log iff:
        cand_last_term > voter_last_term OR
        (cand_last_term == voter_last_term and cand_last_index >= voter_last_index)
        """
        if cand_last_term != voter_last_term:
            return cand_last_term > voter_last_term
        return cand_last_index >= voter_last_index

    @classmethod
    def evaluate_request_vote(
        cls,
        voter: RaftNodeRecord,
        candidate_id: str,
        candidate_term: int,
        cand_last_term: int,
        cand_last_index: int,
    ) -> Tuple[bool, str]:
        """
        Evaluate whether voter grants vote to candidate under standard Raft safety rules.
        """
        # Rule 1: Term check
        if candidate_term < voter.current_term:
            return False, "DENIED_CANDIDATE_TERM_STALE"

        # If candidate has strictly higher term, voter updates term and resets voted_for
        effective_voted_for = voter.voted_for
        if candidate_term > voter.current_term:
            effective_voted_for = None

        # Rule 2: Already voted for someone else in this term
        if effective_voted_for is not None and effective_voted_for != candidate_id:
            return False, "DENIED_ALREADY_VOTED_IN_TERM"

        # Rule 3: Log Up-To-Date rule
        up_to_date = cls.is_candidate_log_up_to_date(
            cand_last_term=cand_last_term,
            cand_last_index=cand_last_index,
            voter_last_term=voter.last_log_term,
            voter_last_index=voter.last_log_index,
        )
        if not up_to_date:
            return False, "DENIED_VOTER_LOG_MORE_UP_TO_DATE"

        return True, "VOTE_GRANTED"

    @classmethod
    def evaluate_partition_scenario(cls) -> Dict[str, Any]:
        """
        Trace scenario: 5-node cluster {A, B, C, D, E} partitioned 2 | 3:
        Minority partition: {A, B}
        Majority partition: {C, D, E}
        """
        # Initial logs at Term 1
        nodes = {
            "A": RaftNodeRecord("A", 1, "A", [RaftLogEntry(1, 1, "x=1")]),
            "B": RaftNodeRecord("B", 1, "A", [RaftLogEntry(1, 1, "x=1")]),
            "C": RaftNodeRecord("C", 1, "A", [RaftLogEntry(1, 1, "x=1")]),
            "D": RaftNodeRecord("D", 1, "A", [RaftLogEntry(1, 1, "x=1")]),
            "E": RaftNodeRecord("E", 1, "A", [RaftLogEntry(1, 1, "x=1")]),
        }

        # Node A (in minority) attempts write in Term 1
        # Reaches only A and B (2 nodes < majority of 3). Cannot commit!
        minority_commit_possible = False

        # Node C (in majority) times out, starts election for Term 2
        # C requests votes from D and E
        votes_for_C = ["C"]  # C votes for self
        for voter_id in ["D", "E"]:
            voter = nodes[voter_id]
            granted, reason = cls.evaluate_request_vote(
                voter=voter,
                candidate_id="C",
                candidate_term=2,
                cand_last_term=1,
                cand_last_index=1,
            )
            if granted:
                votes_for_C.append(voter_id)

        majority_won = len(votes_for_C) >= 3

        # Stale candidate test: Candidate X with old term tries to run against D
        granted_stale, reason_stale = cls.evaluate_request_vote(
            voter=nodes["D"],
            candidate_id="X",
            candidate_term=2,
            cand_last_term=0,
            cand_last_index=0,
        )

        return {
            "cluster_nodes": ["A", "B", "C", "D", "E"],
            "partition": {"minority": ["A", "B"], "majority": ["C", "D", "E"]},
            "minority_can_commit_new_entries": minority_commit_possible,
            "majority_candidate": "C",
            "votes_granted_to_C": votes_for_C,
            "majority_candidate_elected": majority_won,
            "stale_candidate_rejected": not granted_stale,
            "stale_rejection_reason": reason_stale,
            "flp_boundary_notes": (
                "Within Raft's stated crash-failure/non-Byzantine model, its safety argument "
                "does not require a known fixed message-delay bound. Progress requires additional "
                "communication/timing conditions that allow a stable election and quorum exchange. "
                "Randomized election timeouts reduce repeated collisions but DO NOT disprove FLP."
            ),
            "safety_vs_majority_alone": (
                "Majority-set overlap ALONE proves only a set-intersection fact. "
                "Election Safety also relies on the at-most-one-vote-per-term rule. "
                "Leader Completeness additionally relies on Raft's election restriction plus "
                "the log-matching/commit rules. This worksheet checks bounded ingredients, "
                "not the paper's complete safety proof."
            ),
        }


# ==============================================================================
# Trace Family 4: Consistency History Classification & Precedence Oracles
# ==============================================================================

@dataclass
class Operation:
    op_id: str
    client_id: str
    op_type: str        # "W" (write) or "R" (read)
    key: str
    value: Any
    inv_time: float     # Real-time invocation bound
    resp_time: float    # Real-time response bound


class ConsistencyEvaluator:
    """
    Bounded single-register history evaluator.

    The checker reasons from invocation/response precedence on one course-owned
    worksheet timeline. It does not compare independent machine wall clocks.
    """

    @staticmethod
    def precedes(op1: Operation, op2: Operation) -> bool:
        """op1 precedes op2 iff op1 completed before op2 was invoked."""
        return op1.resp_time < op2.inv_time

    @staticmethod
    def _validate_operations(operations: List[Operation]) -> None:
        seen_ids: Set[str] = set()
        for op in operations:
            if op.op_id in seen_ids:
                raise ValueError(f"duplicate operation id: {op.op_id}")
            seen_ids.add(op.op_id)
            if op.op_type not in {"W", "R"}:
                raise ValueError(f"unsupported operation type: {op.op_type}")
            if op.resp_time < op.inv_time:
                raise ValueError(f"response precedes invocation for {op.op_id}")

    @classmethod
    def check_linearizability_single_register(
        cls,
        operations: List[Operation],
        initial_value: Any = 0,
    ) -> Tuple[bool, Optional[str], Optional[Tuple[str, str]]]:
        """
        Exhaustively search linearizations for the small completed histories used by M17.

        A candidate sequential order must preserve every real-time precedence edge.
        Writes replace the register value; reads are legal only when they return the
        current sequential register value. This is a bounded teaching validator, not
        a production general-purpose linearizability checker.
        """
        cls._validate_operations(operations)
        ops = list(operations)
        ids = {op.op_id for op in ops}
        predecessors: Dict[str, Set[str]] = {op.op_id: set() for op in ops}

        for a in ops:
            for b in ops:
                if a.op_id != b.op_id and cls.precedes(a, b):
                    predecessors[b.op_id].add(a.op_id)

        # Preserve per-client program order for well-formed course histories.
        by_client: Dict[str, List[Operation]] = {}
        for op in ops:
            by_client.setdefault(op.client_id, []).append(op)
        for client_ops in by_client.values():
            ordered = sorted(client_ops, key=lambda x: (x.inv_time, x.resp_time, x.op_id))
            for prev, nxt in zip(ordered, ordered[1:]):
                predecessors[nxt.op_id].add(prev.op_id)

        def search(
            placed: Set[str],
            current_value: Any,
        ) -> bool:
            if placed == ids:
                return True

            for op in ops:
                if op.op_id in placed:
                    continue
                if not predecessors[op.op_id].issubset(placed):
                    continue

                if op.op_type == "R":
                    if op.value != current_value:
                        continue
                    next_value = current_value
                else:
                    next_value = op.value

                if search(placed | {op.op_id}, next_value):
                    return True
            return False

        if search(set(), initial_value):
            return True, "LINEARIZABLE", None

        # Provide a bounded witness only when one completed write is forced to be
        # after every other completed-before write by real-time precedence.
        for r in sorted(
            (op for op in ops if op.op_type == "R"),
            key=lambda x: (x.inv_time, x.resp_time),
        ):
            prior_writes = [w for w in ops if w.op_type == "W" and cls.precedes(w, r)]
            forced_latest = [
                w
                for w in prior_writes
                if all(o.op_id == w.op_id or cls.precedes(o, w) for o in prior_writes)
            ]
            if len(forced_latest) == 1 and r.value != forced_latest[0].value:
                latest = forced_latest[0]
                return (
                    False,
                    f"NON_LINEARIZABLE_HISTORY: no legal sequential register order preserves "
                    f"the real-time constraints; read {r.op_id} returned {r.value!r} after "
                    f"forced-latest completed write {latest.op_id} returned {latest.value!r}",
                    (latest.op_id, r.op_id),
                )

        return (
            False,
            "NON_LINEARIZABLE_HISTORY: no legal sequential register order satisfies the "
            "observed reads and real-time precedence constraints",
            None,
        )

    @staticmethod
    def _numeric_version(value: Any, op_id: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                f"{op_id} must use a numeric version token for this bounded session checker"
            )
        return float(value)

    @classmethod
    def check_read_your_writes(
        cls, operations: List[Operation]
    ) -> Tuple[bool, Optional[str], Optional[Tuple[str, str]]]:
        """
        Bounded RYW checker using numeric version tokens.

        A later read by the same client must not observe a version older than that
        client's latest completed write. A newer version from another write is allowed.
        """
        cls._validate_operations(operations)
        by_client: Dict[str, List[Operation]] = {}
        for op in operations:
            by_client.setdefault(op.client_id, []).append(op)

        for cid, client_ops in by_client.items():
            last_written_version: Optional[float] = None
            last_write_op: Optional[Operation] = None
            for op in sorted(client_ops, key=lambda x: (x.inv_time, x.resp_time, x.op_id)):
                if op.op_type == "W":
                    last_written_version = cls._numeric_version(op.value, op.op_id)
                    last_write_op = op
                elif op.op_type == "R" and last_written_version is not None:
                    read_version = cls._numeric_version(op.value, op.op_id)
                    if read_version < last_written_version:
                        return (
                            False,
                            f"RYW_VIOLATION: Client {cid} wrote version "
                            f"{last_written_version:g} in {last_write_op.op_id}, but "
                            f"subsequent read {op.op_id} returned older version "
                            f"{read_version:g}",
                            (last_write_op.op_id, op.op_id),
                        )

        return True, "READ_YOUR_WRITES_SATISFIED", None

    @classmethod
    def check_monotonic_reads(
        cls, operations: List[Operation]
    ) -> Tuple[bool, Optional[str], Optional[Tuple[str, str]]]:
        """Bounded monotonic-read checker using numeric version tokens."""
        cls._validate_operations(operations)
        by_client: Dict[str, List[Operation]] = {}
        for op in operations:
            by_client.setdefault(op.client_id, []).append(op)

        for cid, client_ops in by_client.items():
            previous: Optional[Tuple[Operation, float]] = None
            for op in sorted(client_ops, key=lambda x: (x.inv_time, x.resp_time, x.op_id)):
                if op.op_type != "R":
                    continue
                read_version = cls._numeric_version(op.value, op.op_id)
                if previous is not None and read_version < previous[1]:
                    return (
                        False,
                        f"MONOTONIC_READS_VIOLATION: Client {cid} observed version "
                        f"{previous[1]:g} in {previous[0].op_id}, but later read "
                        f"{op.op_id} observed older version {read_version:g}",
                        (previous[0].op_id, op.op_id),
                    )
                previous = (op, read_version)

        return True, "MONOTONIC_READS_SATISFIED", None


# ==============================================================================
# Helper for trace scenarios
# ==============================================================================

def get_standard_consistency_traces() -> Dict[str, List[Operation]]:
    """
    Returns standard worked-trace histories for L17-03 analysis.
    """
    return {
        "Trace_1_Linearizable": [
            Operation("w1", "client_A", "W", "x", 1, inv_time=1.0, resp_time=3.0),
            Operation("r1", "client_B", "R", "x", 1, inv_time=4.0, resp_time=6.0),
            Operation("w2", "client_A", "W", "x", 2, inv_time=7.0, resp_time=9.0),
            Operation("r2", "client_B", "R", "x", 2, inv_time=10.0, resp_time=12.0),
        ],
        "Trace_2_Stale_Read_Non_Linearizable": [
            Operation("w1", "client_A", "W", "x", 1, inv_time=1.0, resp_time=3.0),
            # r1 invoked at 5.0 (after w1 response at 3.0), but returns stale 0
            Operation("r1", "client_B", "R", "x", 0, inv_time=5.0, resp_time=8.0),
        ],
        "Trace_3_Read_Your_Writes_Violation": [
            Operation("w1", "client_A", "W", "x", 1, inv_time=1.0, resp_time=3.0),
            # Client A immediately reads from lagging replica and gets stale 0
            Operation("r1", "client_A", "R", "x", 0, inv_time=4.0, resp_time=6.0),
        ],
        "Trace_4_Monotonic_Reads_Violation": [
            # Client B reads version 2 from updated replica
            Operation("r1", "client_B", "R", "x", 2, inv_time=2.0, resp_time=4.0),
            # Client B later reads version 1 from lagging replica (time moves backward)
            Operation("r2", "client_B", "R", "x", 1, inv_time=5.0, resp_time=7.0),
        ],
    }
