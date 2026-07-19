#!/usr/bin/env python3
"""Apply filled annotation CSV to TEI as cultural <note> elements.

Date: 26.12.2024

Reads a filled annotation CSV and writes <note type="cultural"> into matching
TEI paragraphs (by xml:id). Output is an annotated TEI file that BaseX can
query for category values.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cultural_tei.apply_annotations import apply_annotations_csv

PROJECT = Path(__file__).resolve().parent

TEI_PATH = PROJECT / "Possession_1000.tei.xml"
CSV_PATH = PROJECT / "possession_annotations_filled.csv"
OUTPUT_PATH = PROJECT / "Possession_1000.annotated.tei.xml"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Filled CSV -> annotated TEI with cultural <note> elements.",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--tei",
        default=str(TEI_PATH),
        help=f"Plain TEI input (default: {TEI_PATH.name})",
    )
    parser.add_argument(
        "--csv",
        default=str(CSV_PATH),
        help=f"Filled annotations CSV (default: {CSV_PATH.name})",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=str(OUTPUT_PATH),
        help=f"Annotated TEI output (default: {OUTPUT_PATH.name})",
    )
    args = parser.parse_args(argv)

    n = apply_annotations_csv(Path(args.tei), Path(args.csv), Path(args.output))
    print(f"Applied annotations to {n} paragraphs -> {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
