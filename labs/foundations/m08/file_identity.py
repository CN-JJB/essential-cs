#!/usr/bin/env python3
"""File identity, hard-link sharing, and open-unlink lifetime observer for M08 L08-01.

Demonstrates:
1. Pathnames/directory entries are names mapped to filesystem metadata objects (inodes).
2. Hard links share identical inode and device numbers; st_nlink reflects directory references.
3. Deleting directory entries (unlink) does not immediately destroy file data while an open
   file descriptor holds an active kernel reference.
4. /proc/self/fd inspection shows kernel descriptor-to-file resolution (Linux-specific).
"""

import json
import os
import stat
import sys
import tempfile
from pathlib import Path


def get_file_identity(path: str | Path) -> dict:
    """Return file identity metadata from stat."""
    st = os.stat(path)
    return {
        "path": str(path),
        "inode": st.st_ino,
        "device": st.st_dev,
        "nlink": st.st_nlink,
        "size": st.st_size,
        "mode": stat.filemode(st.st_mode),
    }


def inspect_proc_fd(fd: int) -> dict:
    """Inspect /proc/self/fd/<fd> if available on Linux hosts."""
    proc_path = Path(f"/proc/self/fd/{fd}")
    result = {
        "proc_fd_path": str(proc_path),
        "available": False,
        "target": None,
        "is_deleted_marked": False,
    }
    if proc_path.exists() or proc_path.is_symlink():
        result["available"] = True
        try:
            target = os.readlink(proc_path)
            result["target"] = target
            result["is_deleted_marked"] = "(deleted)" in target
        except OSError as e:
            result["error"] = str(e)
    return result


def run_identity_experiment(work_dir: str | Path | None = None) -> dict:
    """Execute the bounded file identity and open-unlink reference lifetime experiment."""
    cleanup_temp = False
    if work_dir is None:
        temp_obj = tempfile.TemporaryDirectory(prefix="_run_m08_id_")
        work_path = Path(temp_obj.name)
        cleanup_temp = True
    else:
        work_path = Path(work_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        temp_obj = None

    test_content = b"Essential CS M08 Inode Identity & Reference Lifetime Demonstration\n"
    orig_path = work_path / "original.txt"
    link_path = work_path / "hardlink.txt"

    report = {
        "work_dir": str(work_path),
        "steps": {},
        "verifications": {},
    }

    fd = None
    try:
        # Step 1: Create initial file
        with open(orig_path, "wb") as f:
            f.write(test_content)
            f.flush()

        stat_orig = get_file_identity(orig_path)
        report["steps"]["step1_create"] = stat_orig

        # Step 2: Create hard link
        os.link(orig_path, link_path)
        stat_link = get_file_identity(link_path)
        stat_orig_after_link = get_file_identity(orig_path)
        report["steps"]["step2_hardlink"] = {
            "link_stat": stat_link,
            "orig_stat": stat_orig_after_link,
        }

        # Step 3: Open file descriptor before unlinking
        fd = os.open(orig_path, os.O_RDWR)
        proc_fd_initial = inspect_proc_fd(fd)
        report["steps"]["step3_open_fd"] = {
            "fd": fd,
            "proc_fd": proc_fd_initial,
        }

        # Step 4: Unlink the first name
        os.unlink(orig_path)
        stat_link_after_first_unlink = get_file_identity(link_path)
        report["steps"]["step4_unlink_first_name"] = {
            "orig_exists": orig_path.exists(),
            "link_stat": stat_link_after_first_unlink,
        }

        # Step 5: Unlink the second name (nlink becomes 0)
        os.unlink(link_path)
        proc_fd_after_unlinks = inspect_proc_fd(fd)
        report["steps"]["step5_unlink_all_names"] = {
            "orig_exists": orig_path.exists(),
            "link_exists": link_path.exists(),
            "proc_fd": proc_fd_after_unlinks,
        }

        # Step 6: Read and write through the still-open file descriptor
        os.lseek(fd, 0, os.SEEK_SET)
        read_back_data = os.read(fd, len(test_content))
        append_data = b"Appended bytes while unlinked from all directories\n"
        bytes_written_unlinked = os.write(fd, append_data)
        os.lseek(fd, 0, os.SEEK_SET)
        total_data = os.read(fd, len(test_content) + len(append_data))

        report["steps"]["step6_continued_io"] = {
            "read_back_matches": (read_back_data == test_content),
            "bytes_written_unlinked": bytes_written_unlinked,
            "total_bytes_readable": len(total_data),
        }

        # Verifications
        report["verifications"] = {
            "same_inode": stat_orig["inode"] == stat_link["inode"],
            "same_device": stat_orig["device"] == stat_link["device"],
            "nlink_incremented_on_link": stat_orig_after_link["nlink"] == 2,
            "nlink_decremented_on_unlink": stat_link_after_first_unlink["nlink"] == 1,
            "both_pathnames_removed": (not orig_path.exists()) and (not link_path.exists()),
            "open_fd_io_succeeded": read_back_data == test_content and len(total_data) > len(test_content),
        }

    finally:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass
        if cleanup_temp and temp_obj is not None:
            temp_obj.cleanup()

    return report


def main() -> int:
    print("=== Essential CS M08 — File Identity & Reference Lifetime Observer ===")
    report = run_identity_experiment()

    v = report["verifications"]
    s1 = report["steps"]["step1_create"]
    s2 = report["steps"]["step2_hardlink"]["link_stat"]
    s3 = report["steps"]["step3_open_fd"]
    s5 = report["steps"]["step5_unlink_all_names"]
    s6 = report["steps"]["step6_continued_io"]

    print(f"[1] Original file created: inode={s1['inode']}, dev={s1['device']}, nlink={s1['nlink']}")
    print(f"[2] Hard link created:     inode={s2['inode']}, dev={s2['device']}, nlink={s2['nlink']}")
    print(f"    -> Identity verified: same_inode={v['same_inode']}, same_device={v['same_device']}")

    print(f"[3] Open file descriptor:  fd={s3['fd']}")
    if s3["proc_fd"]["available"]:
        print(f"    -> /proc/self/fd/{s3['fd']} points to: {s3['proc_fd']['target']}")

    print("[4] Both directory entries unlinked from disk.")
    print(f"    -> Directory existence: orig={s5['orig_exists']}, link={s5['link_exists']}")
    if s5["proc_fd"]["available"]:
        print(f"    -> /proc/self/fd/{s3['fd']} after unlink: {s5['proc_fd']['target']}")

    print(f"[5] Continued I/O on unlinked open descriptor:")
    print(f"    -> Read initial content match: {s6['read_back_matches']}")
    print(f"    -> Wrote {s6['bytes_written_unlinked']} bytes into unlinked inode")
    print(f"    -> Total readable bytes: {s6['total_bytes_readable']}")
    print(f"[6] Overall verification: {'PASS' if all(v.values()) else 'FAIL'}")

    return 0 if all(v.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
