"""Make the single controlled M00 change: input.text A中 -> A文."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "input.json"


def main() -> int:
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    if data.get("text") != "A中":
        raise SystemExit("refusing change: reset first; expected baseline text 'A中'")
    data["text"] = "A文"
    INPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("changed.field=text old='A中' new='A文'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
