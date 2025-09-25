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

