from __future__ import annotations

import pytest

from sudoku.core import (
    candidates,
    find_empty_with_mrv,
    is_valid_board,
    parse_board,
    solve_board,
    solve_with_uniqueness_check,
)

EASY_SOLUTION = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


@pytest.fixture()
def easy_board() -> list[list[int]]:
    text = """530070000\n600195000\n098000060\n800060003\n400803001\n700020006\n060000280\n000419005\n000080079"""
    return parse_board(text)


def test_is_valid_board(easy_board: list[list[int]]) -> None:
    assert is_valid_board(easy_board)


def test_candidates_mrv(easy_board: list[list[int]]) -> None:
    row, col, options = find_empty_with_mrv(easy_board)
    assert len(options) == 1
    assert options == candidates(easy_board, row, col)


def test_solve_board_returns_expected_solution(easy_board: list[list[int]]) -> None:
    solution = solve_board(easy_board)
    assert solution == EASY_SOLUTION


def test_unsolvable_board_returns_none() -> None:
    text = """105802000\n000000000\n000700000\n020000060\n000080000\n000010000\n000603000\n000000000\n000205000"""
    board = parse_board(text)
    assert solve_board(board) is None


def test_uniqueness_detection() -> None:
    text = """000000100\n000009000\n000000000\n030040000\n050000020\n000080030\n000000000\n000700000\n001000000"""
    board = parse_board(text)
    solution, is_unique = solve_with_uniqueness_check(board)
    assert solution is not None
    assert is_unique is False

