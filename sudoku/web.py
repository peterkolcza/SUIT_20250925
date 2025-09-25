"""Flask web demo for the Sudoku solver."""
from __future__ import annotations

from pathlib import Path
from typing import Any
from collections.abc import Sequence

from flask import Flask, jsonify, render_template, request

from .core import is_valid_board, solve_with_uniqueness_check


class InvalidPayload(ValueError):
    """Exception used to unify error handling for API responses."""


def _load_board(payload: Any) -> list[list[int]]:
    if not isinstance(payload, Sequence):
        raise InvalidPayload("'board' must be a 9x9 array of integers")
    if len(payload) != 9:
        raise InvalidPayload("Board must have 9 rows")

    board: list[list[int]] = []
    for row in payload:
        if not isinstance(row, Sequence) or len(row) != 9:
            raise InvalidPayload("Each row must contain 9 values")
        converted_row: list[int] = []
        for value in row:
            if not isinstance(value, int):
                raise InvalidPayload("Board values must be integers between 0 and 9")
            if value < 0 or value > 9:
                raise InvalidPayload("Board values must be between 0 and 9")
            converted_row.append(value)
        board.append(converted_row)

    return board


def create_app() -> Flask:
    base_dir = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        static_folder=str(base_dir / "static"),
        template_folder=str(base_dir / "templates"),
    )
    app.config["JSON_SORT_KEYS"] = False

    @app.errorhandler(InvalidPayload)
    @app.errorhandler(ValueError)
    def handle_invalid(exc: Exception):  # type: ignore[override]
        return jsonify({"error": str(exc)}), 400

    @app.get("/")
    def index() -> str:
        return render_template("index.html")

    @app.post("/api/solve")
    def api_solve():
        data = request.get_json(silent=True)
        if data is None:
            raise InvalidPayload("Invalid JSON payload")
        if "board" not in data:
            raise InvalidPayload("Missing 'board' in payload")
        board = _load_board(data["board"])
        if not is_valid_board(board):
            return jsonify({"error": "Board has conflicting values"}), 422

        solution, is_unique = solve_with_uniqueness_check(board)

        if solution is None:
            return jsonify({"error": "Puzzle is unsolvable"}), 422

        response = {"solution": solution, "unique": is_unique}
        if not is_unique:
            response["warning"] = "Puzzle admits multiple solutions"
        return jsonify(response)

    @app.post("/api/analyze")
    def api_analyze():
        data = request.get_json(silent=True)
        if data is None:
            raise InvalidPayload("Invalid JSON payload")
        if "board" not in data:
            raise InvalidPayload("Missing 'board' in payload")

        board = _load_board(data["board"])
        if not is_valid_board(board):
            return jsonify({"valid": False, "solvable": False, "message": "Board has conflicting values"})

        solution, is_unique = solve_with_uniqueness_check(board)
        if solution is None:
            return jsonify({"valid": True, "solvable": False, "message": "Puzzle is unsolvable"})

        message = "Puzzle is solvable"
        if is_unique:
            message += " with a unique solution"
        else:
            message += ", but it has multiple solutions"

        return jsonify({
            "valid": True,
            "solvable": True,
            "unique": is_unique,
            "message": message,
        })

    return app


app = create_app()


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True)

