# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class QueryConfigWeekStartsOn(str, enum.Enum):
    SUNDAY = "sunday"
    MONDAY = "monday"

    def visit(self, sunday: typing.Callable[[], T_Result], monday: typing.Callable[[], T_Result]) -> T_Result:
        if self is QueryConfigWeekStartsOn.SUNDAY:
            return sunday()
        if self is QueryConfigWeekStartsOn.MONDAY:
            return monday()
