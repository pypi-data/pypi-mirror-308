# This file was auto-generated by Fern from our API Definition.

import typing
from .aggregate_expr import AggregateExpr
from .sleep_column_expr import SleepColumnExpr
from .activity_column_expr import ActivityColumnExpr
from .workout_column_expr import WorkoutColumnExpr
from .body_column_expr import BodyColumnExpr
from .index_column_expr import IndexColumnExpr
from .group_key_column_expr import GroupKeyColumnExpr
from .sleep_score_value_macro_expr import SleepScoreValueMacroExpr
from .unrecognized_value_macro_expr import UnrecognizedValueMacroExpr

QueryInstructionSelectItem = typing.Union[
    AggregateExpr,
    SleepColumnExpr,
    ActivityColumnExpr,
    WorkoutColumnExpr,
    BodyColumnExpr,
    IndexColumnExpr,
    GroupKeyColumnExpr,
    SleepScoreValueMacroExpr,
    UnrecognizedValueMacroExpr,
]
