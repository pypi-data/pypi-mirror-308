# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ContraceptiveEntryType(str, enum.Enum):
    UNSPECIFIED = "unspecified"
    IMPLANT = "implant"
    INJECTION = "injection"
    IUD = "iud"
    INTRAVAGINAL_RING = "intravaginal_ring"
    ORAL = "oral"
    PATCH = "patch"

    def visit(
        self,
        unspecified: typing.Callable[[], T_Result],
        implant: typing.Callable[[], T_Result],
        injection: typing.Callable[[], T_Result],
        iud: typing.Callable[[], T_Result],
        intravaginal_ring: typing.Callable[[], T_Result],
        oral: typing.Callable[[], T_Result],
        patch: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ContraceptiveEntryType.UNSPECIFIED:
            return unspecified()
        if self is ContraceptiveEntryType.IMPLANT:
            return implant()
        if self is ContraceptiveEntryType.INJECTION:
            return injection()
        if self is ContraceptiveEntryType.IUD:
            return iud()
        if self is ContraceptiveEntryType.INTRAVAGINAL_RING:
            return intravaginal_ring()
        if self is ContraceptiveEntryType.ORAL:
            return oral()
        if self is ContraceptiveEntryType.PATCH:
            return patch()
