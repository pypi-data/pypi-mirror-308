from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from polars.plugins import register_plugin_function

from polars_tor._internal import __version__ as __version__

if TYPE_CHECKING:
    from polars_tor.typing import IntoExprColumn

LIB = Path(__file__).parent


def is_tor_exit_node(expr: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[expr],
        plugin_path=LIB,
        function_name="is_tor_exit_node",
        is_elementwise=True,
    )

