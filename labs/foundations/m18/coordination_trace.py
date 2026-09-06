#!/usr/bin/env python3
"""
Coordination Trace Evaluator for M18: 2PC, Saga, Leases & Fencing Tokens.

Provides bounded, deterministic local trace evaluators for:
1. Classic Two-Phase Commit (2PC):
   - Prepare / Vote / Decision protocol.
   - Participant PREPARED state uncertainty when coordinator decision is unavailable.
   - Clarifies why a prepared participant cannot unilaterally commit or abort under silence.
   - Shows that a participant voting NO can safely abort, proving not every coordinator
     crash blocks everyone forever.
2. Saga Pattern (3-Step Scenario: Create Order -> Reserve Inventory -> Process Payment):
   - Forward actions with configured reverse-order compensations upon failure.
   - Demonstrates intermediate state visibility / lack of isolation (I in ACID).
   - Explains why compensation is semantic forward recovery, not a physical rollback.
3. Distributed Leases & Monotonically Increasing Fencing Tokens:
   - Lease expiry during client pause / GC stall.
   - Fencing token validation at the protected resource boundary.
   - Stale-holder write rejection when presented token < storage highest_token.
   - Explains that fencing is one important resource-boundary mitigation pattern,
     not the only universally correct distributed-lock design.
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ==============================================================================
# 1. Classic Two-Phase Commit (2PC) Evaluator
# ==============================================================================

class TwoPhaseVote(str, Enum):
    YES = "YES"
    NO = "NO"


class TwoPhaseDecision(str, Enum):
    COMMIT = "COMMIT"
    ABORT = "ABORT"
    UNKNOWN = "UNKNOWN"


class ParticipantState(str, Enum):
    INIT = "INIT"
    PREPARED = "PREPARED"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTED"


class CoordinatorState(str, Enum):
    INIT = "INIT"
    PREPARING = "PREPARING"
    COMMIT_DECIDED = "COMMIT_DECIDED"
    ABORT_DECIDED = "ABORT_DECIDED"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTED"


class TwoPhaseCommitParticipant:
    """Participant in classic Two-Phase Commit."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.state = ParticipantState.INIT
        self.vote_cast: Optional[TwoPhaseVote] = None
        self.decision_received: TwoPhaseDecision = TwoPhaseDecision.UNKNOWN

    def on_prepare(self, vote: TwoPhaseVote) -> TwoPhaseVote:
        self.vote_cast = vote
        if vote == TwoPhaseVote.YES:
            self.state = ParticipantState.PREPARED
        else:
            self.state = ParticipantState.ABORTED
        return vote

    def on_decision(self, decision: TwoPhaseDecision) -> None:
        self.decision_received = decision
        if decision == TwoPhaseDecision.COMMIT:
            self.state = ParticipantState.COMMITTED
        elif decision == TwoPhaseDecision.ABORT:
            self.state = ParticipantState.ABORTED

    def evaluate_unilateral_action_under_silence(self) -> Dict[str, Any]:
        """
        Evaluates what action this participant can unilaterally take when the
        coordinator decision is unavailable.
        """
        if self.state == ParticipantState.PREPARED:
            return {
                "participant": self.name,
                "state": self.state.value,
                "decision_known": False,
                "can_unilaterally_commit": False,
                "can_unilaterally_abort": False,
                "disposition": "BLOCKED_IN_PREPARED_DECISION_UNKNOWN",
                "reason": (
                    "Participant voted YES and entered PREPARED. Silence does not reveal "
                    "the global atomic-commit outcome: another participant may have caused "
                    "ABORT, or the coordinator may have durably chosen COMMIT. Choosing a "
                    "conflicting local outcome would violate atomic-commit agreement. In "
                    "this classic PREPARED/decision-unknown trace, the participant cannot "
                    "choose COMMIT or ABORT from silence alone."
                ),
                "recovery_requirement": (
                    "Requires coordinator recovery log or cooperative termination protocol "
                    "querying other participants."
                ),
            }
        elif self.state == ParticipantState.ABORTED and self.vote_cast == TwoPhaseVote.NO:
            return {
                "participant": self.name,
                "state": self.state.value,
                "decision_known": True,
                "can_unilaterally_commit": False,
                "can_unilaterally_abort": True,
                "disposition": "UNILATERAL_ABORT_SAFE",
                "reason": (
                    "Participant voted NO. Because 2PC requires unanimous YES to commit, "
                    "the transaction can NEVER commit. This participant can safely abort "
                    "unilaterally without waiting for coordinator or peers."
                ),
                "recovery_requirement": "None.",
            }
        else:
            return {
                "participant": self.name,
                "state": self.state.value,
                "decision_known": self.decision_received != TwoPhaseDecision.UNKNOWN,
                "can_unilaterally_commit": self.state == ParticipantState.COMMITTED,
                "can_unilaterally_abort": self.state == ParticipantState.ABORTED,
                "disposition": "DECIDED",
                "reason": f"Participant already reached terminal state {self.state.value}.",
                "recovery_requirement": "None.",
            }


class TwoPhaseCommitCoordinator:
    """Coordinator executing classic Two-Phase Commit with scripted failure injection."""

    def __init__(self, participants: List[TwoPhaseCommitParticipant]) -> None:
        self.participants = {p.name: p for p in participants}
        self.state = CoordinatorState.INIT
        self.durable_log: Optional[TwoPhaseDecision] = None

    def execute_transaction(
        self,
        votes: Dict[str, TwoPhaseVote],
        crash_before_delivery_to: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Executes 2PC across participants.
        Phase 1: Send Prepare, collect votes.
        Decision: Commit if all YES, else Abort. Recorded durably.
        Phase 2: Deliver the decision, with scripted decision unavailability for selected participants. This models a participant missing the decision; it is not a literal ordered simulation of one coordinator process continuing after it has physically crashed.
        """
        if crash_before_delivery_to is None:
            crash_before_delivery_to = []

        self.state = CoordinatorState.PREPARING
        collected_votes: Dict[str, TwoPhaseVote] = {}

        # Phase 1: Prepare
        for name, p in self.participants.items():
            vote = votes.get(name, TwoPhaseVote.NO)
            cast_vote = p.on_prepare(vote)
            collected_votes[name] = cast_vote

        # Coordinator Decision Rule: Unanimous YES => COMMIT, else ABORT
        all_yes = all(v == TwoPhaseVote.YES for v in collected_votes.values())
        if all_yes:
            self.durable_log = TwoPhaseDecision.COMMIT
            self.state = CoordinatorState.COMMIT_DECIDED
        else:
            self.durable_log = TwoPhaseDecision.ABORT
            self.state = CoordinatorState.ABORT_DECIDED

        # Phase 2: Decision Broadcast with scripted delivery failure
        delivered: Dict[str, bool] = {}
        for name, p in self.participants.items():
            if name in crash_before_delivery_to:
                # Scripted: this participant does not receive the coordinator decision.
                delivered[name] = False
            else:
                p.on_decision(self.durable_log)
                delivered[name] = True

        all_delivered = all(delivered.values())
        if all_delivered:
            self.state = (
                CoordinatorState.COMMITTED
                if self.durable_log == TwoPhaseDecision.COMMIT
                else CoordinatorState.ABORTED
            )

        # Evaluate each participant's standing
        participant_reports = {
            name: p.evaluate_unilateral_action_under_silence()
            for name, p in self.participants.items()
        }

        return {
            "coordinator_state": self.state.value,
            "durable_log_decision": (
                self.durable_log.value if self.durable_log else None
            ),
            "votes": {k: v.value for k, v in collected_votes.items()},
            "delivered": delivered,
            "participants": participant_reports,
        }


# ==============================================================================
# 2. Saga Pattern (Compensating Transactions) & Isolation Anomaly Evaluator
# ==============================================================================

class SagaStep:
    """One bounded step in a Saga with its forward action and compensation."""

    def __init__(
        self,
        name: str,
        forward_fn: Callable[[], Dict[str, Any]],
        compensate_fn: Callable[[], Dict[str, Any]],
    ) -> None:
        self.name = name
        self.forward_fn = forward_fn
        self.compensate_fn = compensate_fn
        self.forward_executed = False
        self.compensated = False


class SagaExecutionResult:
    def __init__(self) -> None:
        self.completed_steps: List[str] = []
        self.failed_step: Optional[str] = None
        self.failure_reason: Optional[str] = None
        self.compensated_steps: List[str] = []
        self.intermediate_state_observed: Optional[Dict[str, Any]] = None
        self.final_state: Dict[str, Any] = {}
        self.success: bool = False


class CourseSagaScenario:
    """
    3-Step Saga scenario: Create Order -> Reserve Inventory -> Process Payment.
    Features:
    - Injected failure at Step 3 (Process Payment).
    - Compensating chain in configured reverse order (Step 2 -> Step 1).
    - Concurrent observer hook exposing already-applied intermediate Saga state / lack of workflow-wide isolation.
    """

    def __init__(self, initial_stock: int = 10) -> None:
        self.stock = initial_stock
        self.orders: Dict[str, Dict[str, Any]] = {}
        self.payments: Dict[str, Dict[str, Any]] = {}
        self.logs: List[str] = []

    def get_state(self) -> Dict[str, Any]:
        return {
            "stock": self.stock,
            "orders": dict(self.orders),
            "payments": dict(self.payments),
        }

    def execute_saga(
        self,
        order_id: str,
        fail_at_step3: bool = True,
        inspect_between_step2_and_3: bool = True,
    ) -> SagaExecutionResult:
        result = SagaExecutionResult()
        executed_steps: List[SagaStep] = []

        # Step 1: Create Order
        def forward_create_order() -> Dict[str, Any]:
            self.orders[order_id] = {"status": "PENDING"}
            self.logs.append(f"Step 1: Order {order_id} created with status PENDING")
            return {"order_id": order_id, "status": "PENDING"}

        def compensate_create_order() -> Dict[str, Any]:
            self.orders[order_id] = {"status": "CANCELLED"}
            self.logs.append(f"Compensate Step 1: Order {order_id} cancelled")
            return {"order_id": order_id, "status": "CANCELLED"}

        step1 = SagaStep("CreateOrder", forward_create_order, compensate_create_order)

        # Step 2: Reserve Inventory
        def forward_reserve_inventory() -> Dict[str, Any]:
            if self.stock < 1:
                raise ValueError("Out of stock")
            self.stock -= 1
            self.logs.append(f"Step 2: Inventory reserved for {order_id}, stock now {self.stock}")
            return {"order_id": order_id, "stock": self.stock}

        def compensate_reserve_inventory() -> Dict[str, Any]:
            self.stock += 1
            self.logs.append(f"Compensate Step 2: Inventory released for {order_id}, stock restored to {self.stock}")
            return {"order_id": order_id, "stock": self.stock}

        step2 = SagaStep("ReserveInventory", forward_reserve_inventory, compensate_reserve_inventory)

        # Step 3: Process Payment
        def forward_process_payment() -> Dict[str, Any]:
            if fail_at_step3:
                raise RuntimeError("PAYMENT_DECLINED_INSUFFICIENT_FUNDS")
            self.payments[order_id] = {"status": "CAPTURED", "amount": 99.0}
            self.orders[order_id]["status"] = "CONFIRMED"
            self.logs.append(f"Step 3: Payment captured for {order_id}")
            return {"order_id": order_id, "payment_status": "CAPTURED"}

        def compensate_process_payment() -> Dict[str, Any]:
            if order_id in self.payments:
                self.payments[order_id]["status"] = "REFUNDED"
                self.logs.append(f"Compensate Step 3: Payment refunded for {order_id}")
            return {"order_id": order_id, "payment_status": "REFUNDED"}

        step3 = SagaStep("ProcessPayment", forward_process_payment, compensate_process_payment)

        # Execution Sequence
        steps = [step1, step2, step3]
        for idx, step in enumerate(steps):
            # Concurrent observation hook between Step 2 and Step 3
            if idx == 2 and inspect_between_step2_and_3:
                # An external observer queries the system right here
                result.intermediate_state_observed = {
                    "checkpoint": "BETWEEN_STEP_2_AND_STEP_3",
                    "order_status": self.orders.get(order_id, {}).get("status"),
                    "stock_observed": self.stock,
                    "explanation": (
                        "External observer sees already-applied Saga step state: inventory is "
                        "decremented and order is pending before the payment outcome is known. "
                        "This fixture therefore lacks one ACID isolation boundary across the "
                        "whole workflow; this is not an uncommitted database dirty read."
                    ),
                }

            try:
                step.forward_fn()
                step.forward_executed = True
                executed_steps.append(step)
                result.completed_steps.append(step.name)
            except Exception as exc:
                result.failed_step = step.name
                result.failure_reason = str(exc)
                self.logs.append(f"FAILURE at {step.name}: {exc}. Triggering compensations.")
                break

        # If any step failed, execute compensations for completed steps in reverse order
        if result.failed_step is not None:
            result.success = False
            for step in reversed(executed_steps):
                step.compensate_fn()
                step.compensated = True
                result.compensated_steps.append(step.name)
        else:
            result.success = True

        result.final_state = self.get_state()
        return result


# ==============================================================================
# 3. Distributed Leases & Monotonically Increasing Fencing Tokens
# ==============================================================================

class DistributedLockLease:
    def __init__(self, holder: str, token: int, valid: bool = True) -> None:
        self.holder = holder
        self.token = token
        self.valid = valid


class FencedStorageEngine:
    """
    Storage resource validating monotonically increasing fencing tokens.
    Rejects any write presenting a token strictly lower than the recorded highest token.
    """

    def __init__(self) -> None:
        self.highest_token = 0
        self.records: Dict[str, Any] = {}
        self.rejections: List[Dict[str, Any]] = []
        self.writes: List[Dict[str, Any]] = []

    def write(self, key: str, value: Any, presented_token: int, client_id: str) -> Dict[str, Any]:
        """
        Validates the course fencing-order rule:
        If presented_token < highest_token => REJECT as superseded.
        Else => ACCEPT, update highest_token = presented_token, store value.

        This checker validates ordering only. It does not authenticate token issuance and it does not know that a lease expired unless a higher token has already reached the resource.
        """
        if presented_token < self.highest_token:
            record = {
                "action": "REJECT_STALE_WRITE",
                "client_id": client_id,
                "key": key,
                "presented_token": presented_token,
                "highest_token": self.highest_token,
                "reason": (
                    f"FENCING_TOKEN_VIOLATION: Token {presented_token} is strictly less "
                    f"than storage highest_token {self.highest_token}. Lease has expired "
                    "and a newer lease holder has already taken precedence."
                ),
            }
            self.rejections.append(record)
            return record

        self.highest_token = presented_token
        self.records[key] = value
        record = {
            "action": "ACCEPT_WRITE",
            "client_id": client_id,
            "key": key,
            "value": value,
            "presented_token": presented_token,
            "highest_token": self.highest_token,
        }
        self.writes.append(record)
        return record


class LeaseLockService:
    """Lock service issuing leases with monotonically increasing fencing tokens."""

    def __init__(self) -> None:
        self._current_token = 0
        self.active_lease: Optional[DistributedLockLease] = None

    def acquire_lease(self, holder: str) -> DistributedLockLease:
        self._current_token += 1
        lease = DistributedLockLease(holder=holder, token=self._current_token, valid=True)
        self.active_lease = lease
        return lease

    def expire_lease(self, lease: DistributedLockLease) -> None:
        lease.valid = False
        if self.active_lease is lease:
            self.active_lease = None
