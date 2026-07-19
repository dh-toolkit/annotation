#!/usr/bin/env python3
"""Run queries/*.xq via BaseX and write *-basex.html / CSV outputs.

Date: 10.01.2025

Locates BaseX (portable install or PATH), runs the project XQuery scripts,
and writes category-summary-basex.html, cultural-annotations-report-basex.html,
and possession_annotations_basex.csv.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cultural_tei.basex_runner import run_basex_queries
from cultural_tei.install_deps import default_basex_bin, default_java_home

PROJECT = Path(__file__).resolve().parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run BaseX XQuery reports over the annotated TEI.",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--java-home",
        default=None,
        help="JAVA_HOME for BaseX (default: Temurin under LOCALAPPDATA or env)",
    )
    parser.add_argument(
        "--basex-bin",
        default=None,
        help="Folder containing basex.bat (default: LOCALAPPDATA\\BaseX\\…\\bin)",
    )
    args = parser.parse_args(argv)

    java_home = Path(args.java_home) if args.java_home else default_java_home()
    basex_bin = Path(args.basex_bin) if args.basex_bin else default_basex_bin()
    run_basex_queries(PROJECT, java_home=java_home, basex_bin=basex_bin)
    print(
        "Wrote category-summary-basex.html, cultural-annotations-report-basex.html, "
        "possession_annotations_basex.csv",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
