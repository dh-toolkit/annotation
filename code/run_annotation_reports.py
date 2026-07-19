#!/usr/bin/env python3
"""Build HTML and CSV reports from annotated TEI.

Date: 03.01.2025

Reads cultural <note> elements from annotated TEI and writes a passage-level
HTML table, a primary-category summary HTML page, and a CSV export.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cultural_tei.reports import run_annotation_reports

PROJECT = Path(__file__).resolve().parent

TEI_PATH = PROJECT / "Possession_1000.annotated.tei.xml"
HTML_REPORT = PROJECT / "cultural-annotations-report.html"
SUMMARY_HTML = PROJECT / "category-summary.html"
CSV_OUT = PROJECT / "possession_annotations_from_tei.csv"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Annotated TEI -> HTML + CSV annotation reports.",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--tei",
        default=str(TEI_PATH),
        help=f"Annotated TEI (default: {TEI_PATH.name})",
    )
    parser.add_argument(
        "--html-report",
        default=str(HTML_REPORT),
        help=f"Passage HTML report (default: {HTML_REPORT.name})",
    )
    parser.add_argument(
        "--summary",
        default=str(SUMMARY_HTML),
        help=f"Category summary HTML (default: {SUMMARY_HTML.name})",
    )
    parser.add_argument(
        "--csv",
        default=str(CSV_OUT),
        help=f"CSV export (default: {CSV_OUT.name})",
    )
    args = parser.parse_args(argv)

    n = run_annotation_reports(
        Path(args.tei),
        html_report=Path(args.html_report),
        summary_html=Path(args.summary),
        csv_out=Path(args.csv),
    )
    print(f"Wrote reports ({n} passages)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
