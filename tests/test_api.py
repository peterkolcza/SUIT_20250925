from __future__ import annotations

import pytest

from sudoku.core import parse_board
from sudoku.web import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_api_solve_success(client):
    puzzle = """530070000\n600195000\n098000060\n800060003\n400803001\n700020006\n060000280\n000419005\n000080079"""
    board = parse_board(puzzle)
    response = client.post(
        "/api/solve",
        json={"board": board, "check_uniqueness": True},
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["solution"][0][0] == 5
    assert payload["unique"] is True


def test_api_solve_invalid_payload(client):
    response = client.post("/api/solve", json={"board": [[1, 2, 3]]})
    assert response.status_code == 400
    payload = response.get_json()
    assert "error" in payload


def test_api_solve_rejects_conflicting_board(client):
    conflicting_board = [
        [5, 5, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    response = client.post("/api/solve", json={"board": conflicting_board})
    assert response.status_code == 422
    payload = response.get_json()
    assert payload["error"] == "Board has conflicting values"


def test_api_solve_reports_non_unique_solution(client):
    puzzle = """000000100\n000009000\n000000000\n030040000\n050000020\n000080030\n000000000\n000700000\n001000000"""
    board = parse_board(puzzle)
    response = client.post("/api/solve", json={"board": board})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["unique"] is False
    assert "warning" in payload


def test_api_analyze_unsolvable(client):
    puzzle = """105802000\n000000000\n000700000\n020000060\n000080000\n000010000\n000603000\n000000000\n000205000"""
    board = parse_board(puzzle)
    response = client.post("/api/analyze", json={"board": board})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload == {
        "valid": True,
        "solvable": False,
        "message": "Puzzle is unsolvable",
    }


def test_api_analyze_conflicting_board(client):
    conflicting_board = [
        [5, 5, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    response = client.post("/api/analyze", json={"board": conflicting_board})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload == {
        "valid": False,
        "solvable": False,
        "message": "Board has conflicting values",
    }

