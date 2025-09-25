"""Sudoku solver package."""

from .core import (
    parse_board,
    is_valid_board,
    solve_board,
    solve_with_uniqueness_check,
    pretty_print,
)

__all__ = [
    "parse_board",
    "is_valid_board",
    "solve_board",
    "solve_with_uniqueness_check",
    "pretty_print",
]

# Ensure ``python -m sudoku.solve`` executes the CLI entry point even though the
# module lives in :mod:`sudoku.cli`. This keeps the public command aligned with
# the project brief while retaining an intuitive filename.
import importlib
import sys

if "sudoku.solve" not in sys.modules:
    sys.modules[__name__ + ".solve"] = importlib.import_module(".cli", __name__)


def create_app():
    """Provide a convenient shortcut to the Flask app factory."""
    from .web import create_app as _create_app

    return _create_app()

