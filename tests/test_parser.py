from __future__ import annotations

import pytest

from sudoku.core import is_valid_board, parse_board


def test_parse_board_success():
    text = """530070000\n600195000\n098000060\n800060003\n400803001\n700020006\n060000280\n000419005\n000080079"""
    board = parse_board(text)
    assert len(board) == 9
    assert all(len(row) == 9 for row in board)
    assert board[0][0] == 5
    assert is_valid_board(board)


def test_parse_board_rejects_invalid_character():
    text = """530070000\n600195000\n09x000060\n800060003\n400803001\n700020006\n060000280\n000419005\n000080079"""
    with pytest.raises(ValueError):
        parse_board(text)


def test_parse_board_requires_nine_lines():
    text = """123456789\n123456789"""
    with pytest.raises(ValueError):
        parse_board(text)

