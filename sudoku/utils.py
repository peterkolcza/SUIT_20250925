"""Utility helpers for formatting, timing, and development ergonomics."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Iterable, Sequence

BOARD_SIZE = 9
SUBGRID_SIZE = 3
DIGITS = tuple(range(1, 10))

Board = list[list[int]]


def deepcopy_board(board: Sequence[Sequence[int]]) -> Board:
    """Return a defensive copy of a Sudoku board."""
    return [list(row) for row in board]


def format_board(board: Sequence[Sequence[int]], style: str = "grid") -> str:
    """Return a human friendly string representation of a board.

    Parameters
    ----------
    board:
        Two-dimensional iterable containing integers 0-9.
    style:
        Either ``"grid"`` for a pretty textual grid or ``"plain"`` for
        a single-line representation.
    """

    if style not in {"grid", "plain"}:
        raise ValueError("style must be 'grid' or 'plain'")

    if style == "plain":
        return "".join(str(value) for row in board for value in row)

    rows: list[str] = []
    horizontal = "+-------+-------+-------+"
    for r, row in enumerate(board):
        if r % SUBGRID_SIZE == 0:
            rows.append(horizontal)
        chunks = [
            " ".join("." if value == 0 else str(value) for value in row[i : i + SUBGRID_SIZE])
            for i in range(0, BOARD_SIZE, SUBGRID_SIZE)
        ]
        rows.append("| " + " | ".join(chunks) + " |")
    rows.append(horizontal)
    return "\n".join(rows)


def pretty_print(board: Sequence[Sequence[int]], style: str = "grid") -> str:
    """Alias that mirrors the requirement surface in :mod:`sudoku.core`."""

    return format_board(board, style=style)


@dataclass
class BenchmarkResult:
    """Summary of a benchmarking run."""

    board: Path
    iterations: int
    total_seconds: float

    @property
    def average_seconds(self) -> float:
        return self.total_seconds / self.iterations


def run_benchmark(path: str | Path, iterations: int = 5) -> BenchmarkResult:
    """Benchmark the solver against a given puzzle file."""

    from .core import parse_board, solve_board

    puzzle_path = Path(path)
    text = puzzle_path.read_text(encoding="utf-8")
    board = parse_board(text)

    start = perf_counter()
    for _ in range(iterations):
        solved = solve_board(board)
        if solved is None:
            raise ValueError(f"Puzzle {puzzle_path} is unsolvable and cannot be benchmarked")
    duration = perf_counter() - start
    return BenchmarkResult(board=puzzle_path, iterations=iterations, total_seconds=duration)


def flatten_board(board: Sequence[Sequence[int]]) -> list[int]:
    """Flatten a 9x9 board into a list of 81 integers."""

    return [value for row in board for value in row]


def iter_cells() -> Iterable[tuple[int, int]]:
    """Yield all board coordinates as ``(row, column)`` pairs."""

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            yield r, c

