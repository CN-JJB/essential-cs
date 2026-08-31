"""Restore the deterministic baseline input and opaque fixture state."""

from pathlib import Path
import shutil

from activity import accept_record, current_record, load_input, serialize_record
from opaque_store import reset_payload

HERE = Path(__file__).resolve().parent
BASELINE = HERE / "fixtures" / "baseline-input.json"
INPUT = HERE / "input.json"


def main() -> int:
    shutil.copyfile(BASELINE, INPUT)
    record = current_record(accept_record(load_input(INPUT)))
    reset_payload(serialize_record(record))
    print("reset.ok input=baseline state=baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
