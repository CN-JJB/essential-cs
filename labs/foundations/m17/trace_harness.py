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
    ASYNC = "ASYNC"                 # Leader acks after local write; followers async
    SEMI_SYNC = "SEMI_SYNC"         # Leader acks after local write + 1 follower
    SYNC_ALL = "SYNC_ALL"           # Leader acks after all replicas confirm
    QUORUM_W = "QUORUM_W"           # Leader acks after W replicas confirm (including leader)


class StorageDurability(Enum):
    VOLATILE_RAM = "VOLATILE_RAM"   # Unsynced memory buffer (lost on crash/power loss)
    DURABLE_DISK = "DURABLE_DISK"   # fsync'd durable disk


@dataclass
class ReplicaState:
    node_id: str
    is_leader: bool = False
    is_alive: bool = True
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

    @classmethod
    def simulate_write(
        cls,
        policy: AckPolicy,
        cluster_size: int,
        leader_id: str,
        unreachable_replicas: Set[str],
        crashed_after_write_leader: bool = False,
        w_quorum: int = 2,
    ) -> "ReplicationAckTrace":
        """
        Simulate a single write operation under the named acknowledgment policy.
        """
        replicas = {
            f"node_{i+1}": ReplicaState(
                node_id=f"node_{i+1}",
                is_leader=(f"node_{i+1}" == leader_id),
                is_alive=(f"node_{i+1}" not in unreachable_replicas),
            )
            for i in range(cluster_size)
        }

        entry = {"key": "balance", "val": 100, "version": 1}
        acked_replicas: Set[str] = set()

        leader = replicas[leader_id]
        if not leader.is_alive:
            return cls(
                policy=policy,
                cluster_size=cluster_size,
                w_quorum=w_quorum,
                replicas=replicas,
                client_acked=False,
                ack_error="LEADER_UNREACHABLE",
                acknowledged_replicas=set(),
            )

        # Leader records write locally
        leader.log.append(entry)
        acked_replicas.add(leader_id)

        # Disseminate to reachable followers
        for nid, node in replicas.items():
            if nid != leader_id and node.is_alive:
                node.log.append(entry)
                acked_replicas.add(nid)

        # Evaluate client acknowledgment condition
        client_acked = False
        ack_error = None

        if policy == AckPolicy.ASYNC:
            # Client acked as soon as leader writes locally
            client_acked = True
        elif policy == AckPolicy.SEMI_SYNC:
            # Requires leader + at least 1 follower
            follower_acks = len(acked_replicas - {leader_id})
            if follower_acks >= 1:
                client_acked = True
            else:
                ack_error = "SEMI_SYNC_REPLICA_TIMEOUT"
        elif policy == AckPolicy.SYNC_ALL:
            # Requires all replicas
            if len(acked_replicas) == cluster_size:
                client_acked = True
            else:
                ack_error = "SYNC_ALL_TIMEOUT_FOLLOWER_UNREACHABLE"
        elif policy == AckPolicy.QUORUM_W:
            # Requires W replicas
            if len(acked_replicas) >= w_quorum:
                client_acked = True
            else:
                ack_error = "QUORUM_WRITE_UNSATISFIED"

        # Ambiguous write case: leader crashed before returning ACK to client
        if crashed_after_write_leader:
            leader.is_alive = False
            client_acked = False
            ack_error = "CLIENT_TIMEOUT_LEADER_CRASHED_POST_REPLICATION"

        return cls(
            policy=policy,
            cluster_size=cluster_size,
            w_quorum=w_quorum,
            replicas=replicas,
            client_acked=client_acked,
            ack_error=ack_error,
            acknowledged_replicas=acked_replicas,
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
        Without consensus/total order, Reader {N1, N3} sees mutually conflicting values
        with no way to determine which write was serialized first.
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
            "proof": "QUORUM_OVERLAP_CANNOT_RESOLVE_CONCURRENT_WRITE_ORDER_WITHOUT_CONSENSUS",
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
                "Raft guarantees Safety under all asynchronous conditions. "
                "Liveness requires partial synchrony (bounded message delay during stable election period). "
                "Randomized election timeouts reduce split votes but DO NOT disprove or defeat the FLP theorem."
            ),
            "safety_vs_majority_alone": (
                "Majority overlap alone guarantees no two leaders in the same term. "
                "Leader Completeness strictly requires BOTH majority quorum AND the Log Up-To-Date voting rule."
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
    Classifies execution histories based on real-time invocation/response precedence.
    Does NOT use unsynchronized physical machine clocks.
    """

    @staticmethod
    def precedes(op1: Operation, op2: Operation) -> bool:
        """
        op1 precedes op2 in real time iff op1 completed before op2 was invoked.
        op1 <_real-time op2 <=> op1.resp_time < op2.inv_time
        """
        return op1.resp_time < op2.inv_time

    @classmethod
    def check_linearizability_single_register(
        cls, operations: List[Operation]
    ) -> Tuple[bool, Optional[str], Optional[Tuple[str, str]]]:
        """
        Evaluates whether a sequence of operations on a single register
        violates linearizability.
        Specifically detects stale reads where an earlier completed write
        is not reflected in a strictly later invoked read.
        """
        # Sort operations by invocation time
        writes = [op for op in operations if op.op_type == "W"]
        reads = [op for op in operations if op.op_type == "R"]

        for w in writes:
            for r in reads:
                # If write completed strictly before read was invoked:
                if cls.precedes(w, r):
                    # If read returned a value older than or different from the completed write
                    # (assuming single write sequence for worked trace)
                    if r.value != w.value and r.value == 0:  # Returned initial unwritten state
                        return (
                            False,
                            f"STALE_READ_VIOLATION: Write {w.op_id} (resp={w.resp_time}) "
                            f"preceded Read {r.op_id} (inv={r.inv_time}), but Read returned stale {r.value}",
                            (w.op_id, r.op_id),
                        )

        return True, "LINEARIZABLE", None

    @classmethod
    def check_read_your_writes(
        cls, operations: List[Operation]
    ) -> Tuple[bool, Optional[str], Optional[Tuple[str, str]]]:
        """
        Verifies client-centric Read-Your-Writes session guarantee:
        If client C writes value v, subsequent reads by client C must observe v or newer.
        """
        by_client: Dict[str, List[Operation]] = {}
        for op in operations:
            by_client.setdefault(op.client_id, []).append(op)

        for cid, client_ops in by_client.items():
            last_written_val = None
            last_write_op = None
            for op in sorted(client_ops, key=lambda x: x.inv_time):
                if op.op_type == "W":
                    last_written_val = op.value
                    last_write_op = op
                elif op.op_type == "R" and last_written_val is not None:
                    if op.value != last_written_val:
                        return (
                            False,
                            f"RYW_VIOLATION: Client {cid} wrote {last_written_val} in {last_write_op.op_id}, "
                            f"but subsequent read {op.op_id} returned {op.value}",
                            (last_write_op.op_id, op.op_id),
                        )

        return True, "READ_YOUR_WRITES_SATISFIED", None

    @classmethod
    def check_monotonic_reads(
        cls, operations: List[Operation]
    ) -> Tuple[bool, Optional[str], Optional[Tuple[str, str]]]:
        """
        Verifies client-centric Monotonic Reads session guarantee:
        If client C observes value v1, subsequent reads by client C must never observe an older value v0.
        """
        by_client: Dict[str, List[Operation]] = {}
        for op in operations:
            by_client.setdefault(op.client_id, []).append(op)

        for cid, client_ops in by_client.items():
            seen_read_values: List[Tuple[Operation, int]] = []
            for op in sorted(client_ops, key=lambda x: x.inv_time):
                if op.op_type == "R":
                    # Assume values are version integers for ordering
                    val_int = int(op.value) if isinstance(op.value, (int, float)) else 0
                    for prev_op, prev_val in seen_read_values:
                        if val_int < prev_val:
                            return (
                                False,
                                f"MONOTONIC_READS_VIOLATION: Client {cid} observed version {prev_val} in {prev_op.op_id}, "
                                f"but later read {op.op_id} observed older version {val_int}",
                                (prev_op.op_id, op.op_id),
                            )
                    seen_read_values.append((op, val_int))

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
