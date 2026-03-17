#!/usr/bin/env python3
"""
ExtraDataGenerator — generator.py
===================================
Entry point.  Double-click or run without arguments to launch the GUI.
Pass --help for CLI options.

CLI usage
─────────
  python generator.py --rows 200 --seed 42 --out ./output --format both
  python generator.py --rows 500 --seed 7 --cols first_name,last_name,email,integer --no-nulls
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _build_parser() -> argparse.ArgumentParser:
    from core_gen import COLUMN_TYPES, ISSUE_LABELS

    p = argparse.ArgumentParser(
        prog="generator",
        description="ExtraDataGenerator — messy test data factory",
    )
    p.add_argument("--rows",    type=int, default=100,
                   help="Number of data rows (default: 100)")
    p.add_argument("--seed",    type=int, default=42,
                   help="Random seed for reproducibility (default: 42)")
    p.add_argument("--out",     metavar="DIR", default=".",
                   help="Output directory (default: current dir)")
    p.add_argument("--filename", default="test_data",
                   help="Output filename without extension (default: test_data)")
    p.add_argument("--format",  choices=["csv", "xlsx", "both"], default="csv",
                   help="Output format (default: csv)")
    p.add_argument("--cols",    metavar="TYPES",
                   default=",".join(COLUMN_TYPES.keys()),
                   help="Comma-separated column types to include")

    # Issue toggles
    for key in ISSUE_LABELS:
        p.add_argument(
            f"--no-{key.replace('_', '-')}",
            action="store_true",
            help=f"Disable: {ISSUE_LABELS[key]}",
        )

    return p


def main(argv: list[str] | None = None) -> int:
    from core_gen import DataGenerator, COLUMN_TYPES, ISSUE_LABELS

    args    = _build_parser().parse_args(argv)
    col_types = [c.strip() for c in args.cols.split(",") if c.strip() in COLUMN_TYPES]

    if not col_types:
        print("[ERROR] No valid column types specified.", file=sys.stderr)
        return 1

    issues: dict[str, bool] = {}
    for key in ISSUE_LABELS:
        flag = f"no_{key}"
        issues[key] = not getattr(args, flag, False)

    out_path = Path(args.out)
    gen      = DataGenerator(seed=args.seed)

    print(f"\nExtraDataGenerator")
    print(f"  rows={args.rows}  seed={args.seed}  cols={len(col_types)}  format={args.format}")
    print(f"  output → {out_path.resolve()}\n")

    gen.generate(
        rows=args.rows,
        col_types=col_types,
        issues=issues,
        fmt=args.format,
        out_path=out_path,
        filename=args.filename,
    )

    print(gen.get_report())
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1:
        from gui_gen import main as gui_main
        gui_main()
    else:
        sys.exit(main())
