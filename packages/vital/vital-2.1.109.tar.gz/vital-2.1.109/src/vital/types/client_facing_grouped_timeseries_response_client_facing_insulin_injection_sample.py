# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .client_facing_timeseries_group_client_facing_insulin_injection_sample import (
    ClientFacingTimeseriesGroupClientFacingInsulinInjectionSample,
)
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class ClientFacingGroupedTimeseriesResponseClientFacingInsulinInjectionSample(UniversalBaseModel):
    groups: typing.Dict[str, typing.List[ClientFacingTimeseriesGroupClientFacingInsulinInjectionSample]] = (
        pydantic.Field()
    )
    """
    For each matching provider or lab, a list of grouped timeseries values.
    """

    next: typing.Optional[str] = pydantic.Field(default=None)
    """
    The cursor for fetching the next page, or `null` if there is no more data.
    """

    next_cursor: typing.Optional[str] = pydantic.Field(default=None)
    """
    The cursor for fetching the next page, or `null` if there is no more data.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
