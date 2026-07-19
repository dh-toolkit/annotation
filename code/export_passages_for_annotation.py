#!/usr/bin/env python3
"""Export TEI body paragraphs to a CSV for manual or LLM annotation.

Date: 20.12.2024

Reads a TEI file and writes one CSV row per <p xml:id="…"> with empty
category columns (category_primary, category_secondary, cultural_markers,
notes) ready to fill.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cultural_tei.csv_io import export_passages_csv

PROJECT = Path(__file__).resolve().parent

TEI_PATH = PROJECT / "Possession_1000.tei.xml"
OUTPUT_PATH = PROJECT / "possession_passages.csv"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="TEI -> annotation CSV (one row per passage).",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--tei",
        default=str(TEI_PATH),
        help=f"Input TEI (default: {TEI_PATH.name})",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=str(OUTPUT_PATH),
        help=f"Output CSV (default: {OUTPUT_PATH.name})",
    )
    parser.add_argument(
        "--preview-chars",
        type=int,
        default=500,
        metavar="N",
        help="Max characters in text_preview column (default: 500)",
    )
    args = parser.parse_args(argv)

    n = export_passages_csv(
        Path(args.tei),
        Path(args.output),
        preview_chars=args.preview_chars,
    )
    print(f"Exported {n} passages to {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
