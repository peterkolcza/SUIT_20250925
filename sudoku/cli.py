"""Command line interface for the Sudoku solver."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from .core import (
    parse_board,
    pretty_print,
    solve_board,
    solve_with_uniqueness_check,
)
from .utils import run_benchmark


def _read_from_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"Puzzle file not found: {path}") from exc


def _read_from_stdin() -> str:
    data = sys.stdin.read()
    if not data.strip():
        raise ValueError("No puzzle data provided via stdin")
    return data


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Solve Sudoku puzzles deterministically")
    parser.add_argument(
        "--format",
        choices=["grid", "plain"],
        default="grid",
        help="Output format for the solved board",
    )
    parser.add_argument(
        "--check-unique",
        action="store_true",
        help="Verify whether the puzzle has a unique solution",
    )
    parser.add_argument(
        "--bench",
        metavar="PATH",
        help="Run the benchmark using the puzzle at PATH",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=5,
        help="Number of iterations to use for benchmarking (default: 5)",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--file", type=Path, help="Path to a puzzle text file")
    group.add_argument(
        "--stdin",
        action="store_true",
        help="Read puzzle text from standard input",
    )

    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)

    if args.bench:
        result = run_benchmark(args.bench, iterations=args.iterations)
        print(
            f"Benchmark: {result.board} -> {result.iterations} iterations "
            f"in {result.total_seconds:.3f}s (avg {result.average_seconds:.3f}s)"
        )
        return 0

    if args.file:
        puzzle_text = _read_from_file(args.file)
    elif args.stdin:
        puzzle_text = _read_from_stdin()
    else:
        raise SystemExit("Specify --file or --stdin to provide a puzzle")

    try:
        board = parse_board(puzzle_text)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.check_unique:
        solution, is_unique = solve_with_uniqueness_check(board)
    else:
        solution = solve_board(board)
        is_unique = False

    if solution is None:
        print("Puzzle is unsolvable", file=sys.stderr)
        return 1

    print(pretty_print(solution, style=args.format))
    if args.check_unique:
        note = "unique" if is_unique else "not unique"
        print(f"Solution is {note}.")

    return 0


if __name__ == "__main__":  # pragma: no cover - convenience for manual runs
    raise SystemExit(main())

