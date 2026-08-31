"""Course-supplied opaque save/load boundary for the M00-M01 activity.

Learners in M00-M01 use only save_payload/load_payload. The storage mechanism is
intentionally outside this activity's teaching scope.
"""

from pathlib import Path

_STATE_DIR = Path(__file__).resolve().parent / ".activity_state"
_STATE_FILE = _STATE_DIR / "payload.bin"


def save_payload(payload: bytes) -> None:
    _STATE_DIR.mkdir(exist_ok=True)
    _STATE_FILE.write_bytes(payload)


def load_payload() -> bytes:
    return _STATE_FILE.read_bytes()


def reset_payload(payload: bytes) -> None:
    _STATE_DIR.mkdir(exist_ok=True)
    _STATE_FILE.write_bytes(payload)
