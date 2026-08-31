#!/usr/bin/env python3
"""Deterministic M02 activity: operation growth, interface trade-offs, and correctness.

Standard-library only. The counted operations are explicit teaching-model operations,
not elapsed milliseconds or claims about Python interpreter internals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


ASYMPTOTIC_LABELS = {
    "one_pass": "O(n)",
    "nested_pairs": "O(n^2)",
    "halving": "O(log n)",
    "linear_lookup": "O(n)",
    "indexed_lookup_model": "O(1) average-case logical probe model",
}


@dataclass(frozen=True)
class Record:
    key: str
    value: int


def make_records(n: int) -> list[Record]:
    """Create a deterministic collection with unique keys r0000, r0001, ... ."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return [Record(key=f"r{i:04d}", value=i * 10) for i in range(n)]


def one_pass_count(records: Iterable[Record]) -> int:
    """Count one visit per record."""
    return sum(1 for _ in records)


def nested_pair_count(n: int) -> int:
    """Count unordered pair comparisons: n(n-1)/2."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return n * (n - 1) // 2


def halving_steps(n: int) -> int:
    """Count repeated halvings needed to reduce n to at most 1.

    For powers of two this is exactly log2(n). For other positive n, integer
    floor-halving is used as a transparent teaching model.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    steps = 0
    remaining = n
    while remaining > 1:
        remaining //= 2
        steps += 1
    return steps


def linear_lookup(records: list[Record], key: str) -> tuple[Record | None, int]:
    """Return exact-key result and the number of key comparisons."""
    comparisons = 0
    for record in records:
        comparisons += 1
        if record.key == key:
            return record, comparisons
    return None, comparisons


def build_index(records: list[Record]) -> tuple[dict[str, int], int]:
    """Build key -> list-position index and count one index insertion per record."""
    index: dict[str, int] = {}
    insertions = 0
    for position, record in enumerate(records):
        index[record.key] = position
        insertions += 1
    return index, insertions


def indexed_lookup(
    records: list[Record], index: dict[str, int], key: str
) -> tuple[Record | None, int]:
    """Return result and one logical key-probe count.

    This count deliberately models the interface-level probe only. It does not claim
    that hashing, equality, memory access, or Python execution is literally one
    machine operation or free.
    """
    logical_probes = 1
    position = index.get(key)
    if position is None:
        return None, logical_probes
    return records[position], logical_probes


def invariant_holds(records: list[Record], index: dict[str, int]) -> bool:
    """Collection invariant: unique keys and an exact key->position index."""
    keys = [record.key for record in records]
    if len(keys) != len(set(keys)):
        return False
    if set(index) != set(keys):
        return False
    for key, position in index.items():
        if position < 0 or position >= len(records):
            return False
        if records[position].key != key:
            return False
    return True


def flawed_update_duplicate(
    records: list[Record], index: dict[str, int], key: str, new_value: int
) -> None:
    """Intentionally flawed update: append a duplicate and repoint the index."""
    records.append(Record(key=key, value=new_value))
    index[key] = len(records) - 1


def correct_update(
    records: list[Record], index: dict[str, int], key: str, new_value: int
) -> bool:
    """Update an existing key in place; return False and change nothing if missing."""
    position = index.get(key)
    if position is None:
        return False
    records[position] = Record(key=key, value=new_value)
    return True


def baseline_state(n: int = 8) -> tuple[list[Record], dict[str, int]]:
    records = make_records(n)
    index, _ = build_index(records)
    return records, index


def format_record(record: Record | None) -> str:
    if record is None:
        return "None"
    return f"{record.key}:{record.value}"


def command_reset() -> None:
    records, index = baseline_state()
    print("RESET n=8")
    print(f"RESET invariant={invariant_holds(records, index)}")
    print(f"RESET first={format_record(records[0])} last={format_record(records[-1])}")


def command_baseline() -> None:
    records, index = baseline_state()
    print(f"BASELINE n={len(records)}")
    print(f"BASELINE invariant={invariant_holds(records, index)}")
    print("BASELINE keys=" + ",".join(record.key for record in records))


def command_counts() -> None:
    print("COUNTS model=explicit teaching operations; not elapsed milliseconds")
    print("COUNTS n one_pass nested_pairs halving_steps")
    for n in (8, 16, 32, 64):
        print(f"COUNTS {n} {one_pass_count(make_records(n))} {nested_pair_count(n)} {halving_steps(n)}")
    print(
        "COUNTS labels "
        f"one_pass={ASYMPTOTIC_LABELS['one_pass']} "
        f"nested_pairs={ASYMPTOTIC_LABELS['nested_pairs']} "
        f"halving={ASYMPTOTIC_LABELS['halving']}"
    )


def command_compare() -> None:
    print("LOOKUP counted_operation=list:key_comparison,index:logical_key_probe")
    print("LOOKUP n target linear_count indexed_count index_build_count")
    for n in (8, 64, 1024):
        records = make_records(n)
        target = records[-1].key
        index, build_count = build_index(records)
        linear_record, linear_count = linear_lookup(records, target)
        indexed_record, indexed_count = indexed_lookup(records, index, target)
        assert linear_record == indexed_record
        print(f"LOOKUP {n} {target} {linear_count} {indexed_count} {build_count}")
    print("LOOKUP note=indexed_count is a logical interface probe, not free machine work")


def command_break() -> None:
    records, index = baseline_state()
    key = "r0002"
    print(f"BREAK before.invariant={invariant_holds(records, index)}")
    print(f"BREAK counterexample=duplicate-update key={key} new_value=999")
    flawed_update_duplicate(records, index, key, 999)
    linear_record, linear_count = linear_lookup(records, key)
    indexed_record, indexed_count = indexed_lookup(records, index, key)
    print(f"BREAK after.invariant={invariant_holds(records, index)}")
    print(f"BREAK linear={format_record(linear_record)} comparisons={linear_count}")
    print(f"BREAK indexed={format_record(indexed_record)} logical_probes={indexed_count}")
    print(f"BREAK paths_agree={linear_record == indexed_record}")


def command_correct() -> None:
    records, index = baseline_state()
    key = "r0002"
    updated = correct_update(records, index, key, 999)
    linear_record, _ = linear_lookup(records, key)
    indexed_record, _ = indexed_lookup(records, index, key)
    missing_before = list(records)
    missing_index_before = dict(index)
    missing_updated = correct_update(records, index, "missing", 777)
    missing_unchanged = records == missing_before and index == missing_index_before
    print(f"CORRECT updated={updated} key={key}")
    print(f"CORRECT invariant={invariant_holds(records, index)}")
    print(f"CORRECT linear={format_record(linear_record)} indexed={format_record(indexed_record)}")
    print(f"CORRECT paths_agree={linear_record == indexed_record}")
    print(f"CORRECT missing.updated={missing_updated} unchanged={missing_unchanged}")


def command_flow() -> None:
    command_reset()
    command_baseline()
    command_counts()
    command_compare()
    command_break()
    command_correct()
    command_reset()


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("reset", "baseline", "counts", "compare", "break", "correct", "flow"),
    )
    args = parser.parse_args(argv)

    commands = {
        "reset": command_reset,
        "baseline": command_baseline,
        "counts": command_counts,
        "compare": command_compare,
        "break": command_break,
        "correct": command_correct,
        "flow": command_flow,
    }
    commands[args.command]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
