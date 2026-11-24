#!/usr/bin/env python3
"""List files in a directory tree with their sizes and show a total."""

import argparse
import os
import sys
from pathlib import Path


def human(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            if unit == "B":
                return f"{int(value)} B"
            return f"{value:.1f} {unit}"
        value /= 1024


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List files in a directory tree with their sizes."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--sort",
        choices=["size", "name"],
        default="size",
        help="sort by size or name (default: size)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=0,
        help="print only the N largest files",
    )
    args = parser.parse_args()

    root = Path(args.path)
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 1

    entries = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in filenames:
            file_path = Path(dirpath) / name
            try:
                entries.append((str(file_path), file_path.stat().st_size))
            except OSError:
                continue

    if args.sort == "size":
        entries.sort(key=lambda item: (-item[1], item[0]))
    else:
        entries.sort(key=lambda item: item[0])
    if args.top:
        entries = entries[: args.top]

    total = 0
    for name, size in entries:
        total += size
        print(f"{human(size):>10}  {name}")
    if entries:
        print(f"\ntotal: {len(entries)} files, {human(total)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
