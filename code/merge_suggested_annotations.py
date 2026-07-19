#!/usr/bin/env python3
"""Merge suggested category labels into the filled annotation CSV.

Date: 22.12.2024

Copies category_primary, category_secondary, cultural_markers, and notes from
a suggested CSV into the filled worksheet, matching rows by xml_id.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cultural_tei.csv_io import merge_suggested_csv

PROJECT = Path(__file__).resolve().parent

FILLED_PATH = PROJECT / "possession_annotations_filled.csv"
SUGGESTED_PATH = PROJECT / "possession_annotations_suggested.csv"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Merge suggested CSV labels into filled annotation CSV.",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--filled",
        default=str(FILLED_PATH),
        help=f"Filled / target CSV (default: {FILLED_PATH.name})",
    )
    parser.add_argument(
        "--suggested",
        default=str(SUGGESTED_PATH),
        help=f"Suggested labels CSV (default: {SUGGESTED_PATH.name})",
    )
    args = parser.parse_args(argv)

    n = merge_suggested_csv(Path(args.filled), Path(args.suggested))
    print(f"Merged suggested labels into {args.filled} ({n} rows)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
