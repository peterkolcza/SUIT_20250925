"""Core Sudoku solving logic with MRV heuristic and forward checking."""
from __future__ import annotations

from typing import Iterable, Optional, Sequence, Set

from . import utils

Board = list[list[int]]


def parse_board(text: str) -> Board:
    """Parse a textual Sudoku grid into a 9x9 integer board."""

    if not text:
        raise ValueError("Puzzle text is empty")

    raw_lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(raw_lines) != utils.BOARD_SIZE:
        raise ValueError("Puzzle must contain exactly 9 non-empty lines")

    board: Board = []
    for line in raw_lines:
        if len(line) != utils.BOARD_SIZE:
            raise ValueError("Each line must contain exactly 9 characters")
        row: list[int] = []
        for char in line:
            if char in {"0", "."}:
                row.append(0)
            elif char.isdigit():
                value = int(char)
                if value == 0 or value > 9:
                    raise ValueError("Digits must be between 1 and 9")
                row.append(value)
            else:
                raise ValueError("Unexpected character in puzzle text")
        board.append(row)
    if not is_valid_board(board):
        raise ValueError("Puzzle contains conflicts")
    return board


def is_valid_board(board: Sequence[Sequence[int]]) -> bool:
    """Return ``True`` if the board respects Sudoku constraints."""

    if len(board) != utils.BOARD_SIZE:
        return False
    for row in board:
        if len(row) != utils.BOARD_SIZE:
            return False
        for value in row:
            if not isinstance(value, int) or value < 0 or value > 9:
                return False

    def has_duplicates(values: Iterable[int]) -> bool:
        seen: Set[int] = set()
        for value in values:
            if value == 0:
                continue
            if value in seen:
                return True
            seen.add(value)
        return False

    for row in board:
        if has_duplicates(row):
            return False

    for col in range(utils.BOARD_SIZE):
        if has_duplicates(board[row][col] for row in range(utils.BOARD_SIZE)):
            return False

    for box_row in range(0, utils.BOARD_SIZE, utils.SUBGRID_SIZE):
        for box_col in range(0, utils.BOARD_SIZE, utils.SUBGRID_SIZE):
            cells = (
                board[r][c]
                for r in range(box_row, box_row + utils.SUBGRID_SIZE)
                for c in range(box_col, box_col + utils.SUBGRID_SIZE)
            )
            if has_duplicates(cells):
                return False

    return True


def candidates(board: Sequence[Sequence[int]], row: int, col: int) -> Set[int]:
    """Return the set of legal values for ``board[row][col]``."""

    if board[row][col] != 0:
        return set()

    used = set(board[row])
    used.update(board[r][col] for r in range(utils.BOARD_SIZE))

    start_row = (row // utils.SUBGRID_SIZE) * utils.SUBGRID_SIZE
    start_col = (col // utils.SUBGRID_SIZE) * utils.SUBGRID_SIZE
    for r in range(start_row, start_row + utils.SUBGRID_SIZE):
        for c in range(start_col, start_col + utils.SUBGRID_SIZE):
            used.add(board[r][c])

    return {value for value in utils.DIGITS if value not in used}


def find_empty_with_mrv(board: Sequence[Sequence[int]]) -> Optional[tuple[int, int, Set[int]]]:
    """Return the coordinates of the next cell using MRV heuristic."""

    best_cell: Optional[tuple[int, int, Set[int]]] = None
    best_size = utils.BOARD_SIZE + 1
    for row, col in utils.iter_cells():
        if board[row][col] != 0:
            continue
        options = candidates(board, row, col)
        option_count = len(options)
        if option_count == 0:
            return row, col, options
        if option_count < best_size:
            best_cell = (row, col, options)
            best_size = option_count
            if best_size == 1:
                break
    return best_cell


def _forward_check(board: Sequence[Sequence[int]]) -> bool:
    """Ensure every empty cell still has a candidate."""

    for row, col in utils.iter_cells():
        if board[row][col] == 0 and not candidates(board, row, col):
            return False
    return True


def _search(board: Board) -> Optional[Board]:
    cell = find_empty_with_mrv(board)
    if cell is None:
        return utils.deepcopy_board(board)

    row, col, options = cell
    if not options:
        return None

    for value in sorted(options):
        board[row][col] = value
        if _forward_check(board):
            solution = _search(board)
            if solution is not None:
                board[row][col] = 0
                return solution
        board[row][col] = 0
    return None


def solve_board(board: Sequence[Sequence[int]]) -> Optional[Board]:
    """Solve a Sudoku puzzle using backtracking with forward checking."""

    if not is_valid_board(board):
        raise ValueError("Board is malformed or violates Sudoku rules")

    working = utils.deepcopy_board(board)
    return _search(working)


def _search_multiple(board: Board, limit: int) -> list[Board]:
    solutions: list[Board] = []

    def backtrack() -> None:
        if len(solutions) >= limit:
            return
        cell = find_empty_with_mrv(board)
        if cell is None:
            solutions.append(utils.deepcopy_board(board))
            return
        row, col, options = cell
        if not options:
            return
        for value in sorted(options):
            board[row][col] = value
            if _forward_check(board):
                backtrack()
                if len(solutions) >= limit:
                    break
            board[row][col] = 0
        board[row][col] = 0

    backtrack()
    return solutions


def solve_with_uniqueness_check(board: Sequence[Sequence[int]]) -> tuple[Optional[Board], bool]:
    """Solve the puzzle and report whether the solution is unique."""

    if not is_valid_board(board):
        raise ValueError("Board is malformed or violates Sudoku rules")

    working = utils.deepcopy_board(board)
    solutions = _search_multiple(working, limit=2)
    if not solutions:
        return None, False
    return solutions[0], len(solutions) == 1


def pretty_print(board: Sequence[Sequence[int]], style: str = "grid") -> str:
    """Expose the formatter from :mod:`sudoku.utils`."""

    return utils.pretty_print(board, style=style)

