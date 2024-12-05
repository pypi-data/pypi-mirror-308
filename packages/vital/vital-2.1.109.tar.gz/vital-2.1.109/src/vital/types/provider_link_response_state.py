# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ProviderLinkResponseState(str, enum.Enum):
    SUCCESS = "success"
    ERROR = "error"
    PENDING_PROVIDER_MFA = "pending_provider_mfa"

    def visit(
        self,
        success: typing.Callable[[], T_Result],
        error: typing.Callable[[], T_Result],
        pending_provider_mfa: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ProviderLinkResponseState.SUCCESS:
            return success()
        if self is ProviderLinkResponseState.ERROR:
            return error()
        if self is ProviderLinkResponseState.PENDING_PROVIDER_MFA:
            return pending_provider_mfa()
