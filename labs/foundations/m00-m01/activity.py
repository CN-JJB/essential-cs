"""Deterministic M00-M01 observation surface. Python standard library only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from opaque_store import load_payload, save_payload

HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "input.json"
MAGIC = b"ECS1"
UINT16_MIN = 0
UINT16_MAX = 2**16 - 1
INT16_MIN = -(2**15)
INT16_MAX = 2**15 - 1


def _require_int(name: str, value: Any, low: int, high: int) -> int:
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    if not low <= value <= high:
        raise ValueError(f"{name} out of range [{low}, {high}]: {value}")
    return value


def encode_uint16(value: int, byteorder: str) -> bytes:
    _require_int("uint16", value, UINT16_MIN, UINT16_MAX)
    if byteorder not in {"little", "big"}:
        raise ValueError("byteorder must be 'little' or 'big'")
    return value.to_bytes(2, byteorder=byteorder, signed=False)


def decode_uint16(data: bytes, byteorder: str) -> int:
    if len(data) != 2:
        raise ValueError("uint16 needs exactly 2 bytes")
    if byteorder not in {"little", "big"}:
        raise ValueError("byteorder must be 'little' or 'big'")
    return int.from_bytes(data, byteorder=byteorder, signed=False)


def encode_int16(value: int, byteorder: str) -> bytes:
    _require_int("int16", value, INT16_MIN, INT16_MAX)
    if byteorder not in {"little", "big"}:
        raise ValueError("byteorder must be 'little' or 'big'")
    return value.to_bytes(2, byteorder=byteorder, signed=True)


def decode_int16(data: bytes, byteorder: str) -> int:
    if len(data) != 2:
        raise ValueError("int16 needs exactly 2 bytes")
    if byteorder not in {"little", "big"}:
        raise ValueError("byteorder must be 'little' or 'big'")
    return int.from_bytes(data, byteorder=byteorder, signed=True)


def load_input(path: Path = INPUT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def accept_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Narrow learner-visible interface: validate input and create process-local state."""
    if set(raw) != {"id", "delta", "text"}:
        raise ValueError("record fields must be exactly: id, delta, text")
    record_id = _require_int("id", raw["id"], UINT16_MIN, UINT16_MAX)
    delta = _require_int("delta", raw["delta"], INT16_MIN, INT16_MAX)
    text = raw["text"]
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    text_bytes = text.encode("utf-8")
    if len(text_bytes) > UINT16_MAX:
        raise ValueError("UTF-8 text is too long for the uint16 length field")
    state = {"records": [{"id": record_id, "delta": delta, "text": text}]}
    return state


def current_record(state: dict[str, Any]) -> dict[str, Any]:
    return state["records"][-1]


def serialize_record(record: dict[str, Any], *, byteorder: str = "little") -> bytes:
    text_bytes = record["text"].encode("utf-8")
    return b"".join(
        [
            MAGIC,
            encode_uint16(record["id"], byteorder),
            encode_int16(record["delta"], byteorder),
            encode_uint16(len(text_bytes), byteorder),
            text_bytes,
        ]
    )


def deserialize_record(payload: bytes, *, byteorder: str = "little") -> dict[str, Any]:
    if len(payload) < 10:
        raise ValueError("record is truncated")
    if payload[:4] != MAGIC:
        raise ValueError("record magic mismatch")
    record_id = decode_uint16(payload[4:6], byteorder)
    delta = decode_int16(payload[6:8], byteorder)
    text_len = decode_uint16(payload[8:10], byteorder)
    if len(payload) != 10 + text_len:
        raise ValueError("record length does not match text_len")
    text = payload[10:].decode("utf-8")
    return {"id": record_id, "delta": delta, "text": text}


def hex_bytes(data: bytes) -> str:
    return " ".join(f"{byte:02x}" for byte in data)


def run_once(*, quiet: bool = False) -> dict[str, Any]:
    raw = load_input()
    state = accept_record(raw)
    record = current_record(state)
    payload = serialize_record(record, byteorder="little")
    save_payload(payload)
    decoded = deserialize_record(payload, byteorder="little")
    if not quiet:
        print(f"INPUT id={raw['id']} delta={raw['delta']} text={raw['text']!r}")
        print("INTERFACE accept_record")
        print(f"STATE records={len(state['records'])} current_text={record['text']!r}")
        print("BOUNDARY save_payload/load_payload (course-supplied; opaque in M00-M01)")
        print(f"OUTPUT bytes={len(payload)} hex={hex_bytes(payload)}")
        print(f"ROUNDTRIP ok={decoded == record}")
    return {"raw": raw, "state": state, "record": record, "payload": payload, "decoded": decoded}


def command_inspect() -> None:
    record = current_record(accept_record(load_input()))
    payload = serialize_record(record)
    text_bytes = record["text"].encode("utf-8")
    fields = [
        ("magic", 0, 4, payload[0:4]),
        ("id", 4, 2, payload[4:6]),
        ("delta", 6, 2, payload[6:8]),
        ("text_len", 8, 2, payload[8:10]),
        ("text", 10, len(text_bytes), payload[10:]),
    ]
    print(f"record.hex={hex_bytes(payload)}")
    for name, offset, size, data in fields:
        print(f"field.{name} offset={offset} size={size} bytes={hex_bytes(data)}")
    print(f"utf8.text={record['text']}")
    print("utf8.code_points=" + " ".join(f"U+{ord(ch):04X}" for ch in record["text"]))
    print(f"utf8.bytes={hex_bytes(text_bytes)}")
    print(f"utf8.byte_count={len(text_bytes)}")
    print(f"python.len_text={len(record['text'])}")


def command_endian() -> None:
    value = 513
    little = encode_uint16(value, "little")
    big = encode_uint16(value, "big")
    print(f"endian.value={value}")
    print(f"endian.little={hex_bytes(little)} decoded={decode_uint16(little, 'little')}")
    print(f"endian.big={hex_bytes(big)} decoded={decode_uint16(big, 'big')}")


def command_break_endian() -> None:
    value = 513
    big = encode_uint16(value, "big")
    wrong = decode_uint16(big, "little")
    print(f"break.endian.bytes={hex_bytes(big)}")
    print(f"break.endian.expected={value} decoded_with_wrong_order={wrong}")


def command_break_utf8() -> None:
    data = "A中".encode("utf-8")[:-1]
    print(f"break.utf8.bytes={hex_bytes(data)}")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"break.utf8.error={exc.__class__.__name__}")
        return
    raise AssertionError("truncated UTF-8 unexpectedly decoded")


def command_ranges() -> None:
    print(f"uint16.range={UINT16_MIN}..{UINT16_MAX}")
    print(f"int16.range={INT16_MIN}..{INT16_MAX}")
    minus_two = encode_int16(-2, "big")
    print(f"int16.-2.bits={int.from_bytes(minus_two, 'big'):016b}")
    print(f"int16.-2.hex={minus_two.hex()}")


def command_break_record() -> None:
    record = current_record(accept_record(load_input()))
    payload = serialize_record(record)
    truncated = payload[:-1]
    print(f"break.record.original_bytes={len(payload)}")
    print(f"break.record.truncated_bytes={len(truncated)}")
    print(f"break.record.hex={hex_bytes(truncated)}")
    try:
        deserialize_record(truncated)
    except (UnicodeDecodeError, ValueError) as exc:
        print(f"break.record.error={exc.__class__.__name__}: {exc}")
        return
    raise AssertionError("truncated record unexpectedly decoded")


def command_load() -> None:
    payload = load_payload()
    record = deserialize_record(payload)
    print(f"LOAD id={record['id']} delta={record['delta']} text={record['text']!r}")
    print("NOTE later retrieval is an observation of this fixture, not proof of durability")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ["run", "inspect", "endian", "break-endian", "break-utf8", "break-record", "ranges", "load"]:
        sub.add_parser(name)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    commands = {
        "run": lambda: run_once(),
        "inspect": command_inspect,
        "endian": command_endian,
        "break-endian": command_break_endian,
        "break-utf8": command_break_utf8,
        "break-record": command_break_record,
        "ranges": command_ranges,
        "load": command_load,
    }
    commands[args.command]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
