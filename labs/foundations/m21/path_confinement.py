#!/usr/bin/env python3
"""
path_confinement.py — Course-owned path-resolution / containment helpers for L21-01.

Required Core mechanism:
    resolve the candidate inside a disposable course-owned tree, then test
    resolved-path ancestry with os.path.commonpath (normcase-aware).

This is a teaching containment relation. It does not prove:
    - that rejecting "../" is enough;
    - that str.startswith(base) proves containment;
    - that one resolve()/realpath() call makes a later open() race-free;
    - that authentication makes a filename trustworthy;
    - that canonicalization prevents every filesystem race.

All paths are synthetic and confined to a TemporaryDirectory the caller owns.
No host-sensitive files are opened.
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class PathConfinementError(ValueError):
    """Raised when a candidate is structurally unusable (e.g. embedded NUL)."""


def _norm(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(path)))


def naive_string_looks_safe(raw: str) -> bool:
    """
    Intentionally incomplete syntactic check.

    Rejects embedded NUL, absolute paths, and a ".." path component.
    Does not inspect the filesystem and therefore cannot see symlink targets.
    """
    if "\x00" in raw:
        return False
    candidate = Path(raw)
    if candidate.is_absolute():
        return False
    for part in Path(raw.replace("\\", "/")).parts:
        if part == "..":
            return False
    return True


def prefix_startswith_looks_contained(authorized_root: Path, candidate: Path) -> bool:
    """
    Demonstrably wrong "containment": raw string prefix comparison.

    Classic sibling-prefix confusion: authorized root ".../data" appears to
    contain ".../data-evil/secret" because the latter string starts with the
    former. Not used as the Required Core decision procedure.
    """
    return _norm(candidate).startswith(_norm(authorized_root))


def is_resolved_contained(authorized_root: Path, resolved_candidate: Path) -> bool:
    """
    Resolved-path ancestry / commonpath parent relationship.

    A candidate is contained iff the longest common path of the resolved
    authorized root and the resolved candidate is exactly the authorized root.
    Different-drive (Windows) or otherwise incomparable paths raise ValueError
    from os.path.commonpath and are treated as not contained.
    """
    root = Path(authorized_root).resolve()
    cand = Path(resolved_candidate)
    try:
        common = os.path.commonpath([_norm(root), _norm(cand)])
    except ValueError:
        return False
    return common == _norm(root)


def join_candidate(authorized_root: Path, raw: str) -> Path:
    """Map a learner-supplied candidate onto the authorized root when relative."""
    if "\x00" in raw:
        raise PathConfinementError("embedded NUL byte is not a valid path candidate")
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    return authorized_root / raw


@dataclass
class ContainmentVerdict:
    candidate: str
    case_id: str
    naive_string_safe: bool
    prefix_startswith_contained: Optional[bool]
    resolved_path: Optional[str]
    resolved_contained: bool
    decision: str
    mechanism: str
    opened_file: bool
    opened_host_sensitive_path: bool
    notes: str
    symlink_dimension: str = "NOT APPLICABLE"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "candidate": self.candidate,
            "case_id": self.case_id,
            "naive_string_safe": self.naive_string_safe,
            "prefix_startswith_contained": self.prefix_startswith_contained,
            "resolved_path": self.resolved_path,
            "resolved_contained": self.resolved_contained,
            "decision": self.decision,
            "mechanism": self.mechanism,
            "opened_file": self.opened_file,
            "opened_host_sensitive_path": self.opened_host_sensitive_path,
            "notes": self.notes,
            "symlink_dimension": self.symlink_dimension,
        }


MECHANISM_LABEL = (
    "Path.resolve() then os.path.commonpath ancestry "
    "(normcase-aware parent relationship); not str.startswith"
)


def classify_candidate(
    authorized_root: Path,
    raw: str,
    case_id: str,
    *,
    read_if_allowed: bool = False,
    symlink_dimension: str = "NOT APPLICABLE",
    extra_notes: str = "",
) -> ContainmentVerdict:
    naive = naive_string_looks_safe(raw)
    prefix: Optional[bool] = None
    resolved: Optional[Path] = None
    notes = extra_notes

    if "\x00" in raw:
        return ContainmentVerdict(
            candidate="<embedded NUL; not printed as a filesystem path>",
            case_id=case_id,
            naive_string_safe=False,
            prefix_startswith_contained=False,
            resolved_path=None,
            resolved_contained=False,
            decision="DENIED",
            mechanism=MECHANISM_LABEL,
            opened_file=False,
            opened_host_sensitive_path=False,
            notes="Embedded NUL rejected before any filesystem open. " + notes,
            symlink_dimension=symlink_dimension,
        )

    try:
        joined = join_candidate(authorized_root, raw)
        prefix = prefix_startswith_looks_contained(authorized_root.resolve(), joined)
        resolved = joined.resolve()
        contained = is_resolved_contained(authorized_root, resolved)
    except PathConfinementError as exc:
        return ContainmentVerdict(
            candidate=raw,
            case_id=case_id,
            naive_string_safe=naive,
            prefix_startswith_contained=False,
            resolved_path=None,
            resolved_contained=False,
            decision="DENIED",
            mechanism=MECHANISM_LABEL,
            opened_file=False,
            opened_host_sensitive_path=False,
            notes=str(exc),
            symlink_dimension=symlink_dimension,
        )
    except (OSError, RuntimeError) as exc:
        return ContainmentVerdict(
            candidate=raw,
            case_id=case_id,
            naive_string_safe=naive,
            prefix_startswith_contained=prefix,
            resolved_path=None,
            resolved_contained=False,
            decision="DENIED",
            mechanism=MECHANISM_LABEL,
            opened_file=False,
            opened_host_sensitive_path=False,
            notes=f"Resolution failed ({type(exc).__name__}); treated as DENIED. {notes}",
            symlink_dimension=symlink_dimension,
        )

    decision = "ALLOWED" if contained else "DENIED"
    opened = False
    if read_if_allowed and contained and resolved is not None and resolved.is_file():
        # Read only after containment, and only the resolved synthetic file.
        resolved.read_bytes()
        opened = True

    return ContainmentVerdict(
        candidate=raw,
        case_id=case_id,
        naive_string_safe=naive,
        prefix_startswith_contained=prefix,
        resolved_path=str(resolved) if resolved is not None else None,
        resolved_contained=contained,
        decision=decision,
        mechanism=MECHANISM_LABEL,
        opened_file=opened,
        opened_host_sensitive_path=False,
        notes=notes,
        symlink_dimension=symlink_dimension,
    )


@dataclass
class SyntheticTree:
    temp_dir: tempfile.TemporaryDirectory
    root: Path
    authorized_root: Path
    allowed_file: Path
    outside_file: Path
    sibling_evil_file: Path
    symlink_path: Optional[Path]
    symlink_disposition: str
    symlink_error: Optional[str] = None
    owned_paths: List[Path] = field(default_factory=list)

    def cleanup(self) -> None:
        self.temp_dir.cleanup()


def _try_symlink(link_path: Path, target: Path) -> Tuple[bool, Optional[str]]:
    try:
        os.symlink(os.fspath(target), os.fspath(link_path))
        return True, None
    except (OSError, NotImplementedError) as exc:
        return False, f"{type(exc).__name__}: {exc}"


def build_synthetic_tree() -> SyntheticTree:
    """
    Build a disposable course-owned tree:

        <tmp>/
          store/                 authorized root
            notes/hello.txt      allowed file
            escape_link -> ../outside.txt   (if the host can create symlinks)
          store-evil/secret.txt  sibling-prefix confusion target
          outside.txt            traversal / symlink escape target
    """
    temp_dir = tempfile.TemporaryDirectory(prefix="ecs-m21-l21-01-")
    root = Path(temp_dir.name)
    authorized = root / "store"
    notes = authorized / "notes"
    notes.mkdir(parents=True)
    allowed = notes / "hello.txt"
    allowed.write_text("synthetic-allowed-payload\n", encoding="utf-8")

    outside = root / "outside.txt"
    outside.write_text("synthetic-outside-payload\n", encoding="utf-8")

    sibling_dir = root / "store-evil"
    sibling_dir.mkdir()
    sibling_file = sibling_dir / "secret.txt"
    sibling_file.write_text("synthetic-sibling-payload\n", encoding="utf-8")

    link_path = authorized / "escape_link"
    created, err = _try_symlink(link_path, outside)
    if created:
        symlink_path: Optional[Path] = link_path
        disposition = "SYMLINK CAPABILITY PASS"
        symlink_error = None
    else:
        symlink_path = None
        disposition = "ENVIRONMENT-BLOCKED / NOT RUN"
        symlink_error = err

    owned = [root, authorized, notes, allowed, outside, sibling_dir, sibling_file]
    if symlink_path is not None:
        owned.append(symlink_path)

    return SyntheticTree(
        temp_dir=temp_dir,
        root=root,
        authorized_root=authorized,
        allowed_file=allowed,
        outside_file=outside,
        sibling_evil_file=sibling_file,
        symlink_path=symlink_path,
        symlink_disposition=disposition,
        symlink_error=symlink_error,
        owned_paths=owned,
    )


def evaluate_standard_cases(tree: SyntheticTree, *, read_if_allowed: bool = True) -> List[ContainmentVerdict]:
    """Deterministic teaching cases for L21-01. No host-sensitive paths."""
    auth = tree.authorized_root
    cases: List[ContainmentVerdict] = []

    cases.append(
        classify_candidate(
            auth,
            "notes/hello.txt",
            "contained-relative",
            read_if_allowed=read_if_allowed,
            extra_notes="Relative path that remains under the authorized root after resolution.",
        )
    )
    cases.append(
        classify_candidate(
            auth,
            "notes/../notes/hello.txt",
            "dotdot-but-still-contained",
            read_if_allowed=read_if_allowed,
            extra_notes="Contains '..' components but resolves back inside the authorized root.",
        )
    )
    cases.append(
        classify_candidate(
            auth,
            "../outside.txt",
            "parent-traversal",
            read_if_allowed=read_if_allowed,
            extra_notes="Relative traversal to a sibling of the authorized root inside the owned temp tree.",
        )
    )
    cases.append(
        classify_candidate(
            auth,
            str(tree.outside_file.resolve()),
            "absolute-outside",
            read_if_allowed=read_if_allowed,
            extra_notes=(
                "Absolute path pointing at a synthetic file inside the owned temp tree, "
                "not at a host-sensitive location."
            ),
        )
    )
    cases.append(
        classify_candidate(
            auth,
            str(tree.sibling_evil_file.resolve()),
            "sibling-prefix",
            read_if_allowed=read_if_allowed,
            extra_notes=(
                "Sibling directory whose string form shares the authorized-root prefix "
                "('store' vs 'store-evil'). startswith is the wrong relation."
            ),
        )
    )
    cases.append(
        classify_candidate(
            auth,
            "notes/hello.txt\x00../outside.txt",
            "embedded-nul",
            read_if_allowed=False,
            extra_notes="Embedded NUL must be rejected before any open().",
        )
    )

    if tree.symlink_path is not None:
        cases.append(
            classify_candidate(
                auth,
                "escape_link",
                "symlink-escape",
                read_if_allowed=read_if_allowed,
                symlink_dimension=tree.symlink_disposition,
                extra_notes=(
                    "Candidate name has no '..' component; naive string checks miss the "
                    "symlink target. Resolution follows the link to a path outside the root."
                ),
            )
        )
    else:
        cases.append(
            ContainmentVerdict(
                candidate="escape_link",
                case_id="symlink-escape",
                naive_string_safe=True,
                prefix_startswith_contained=None,
                resolved_path=None,
                resolved_contained=False,
                decision="BLOCKED / NOT RUN",
                mechanism=MECHANISM_LABEL,
                opened_file=False,
                opened_host_sensitive_path=False,
                notes=(
                    "Host could not create a course-owned symlink "
                    f"({tree.symlink_error}). This dimension is not converted to PASS."
                ),
                symlink_dimension=tree.symlink_disposition,
            )
        )
    return cases
