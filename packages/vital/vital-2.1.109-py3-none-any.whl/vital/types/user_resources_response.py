# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .single_user_resource_response import SingleUserResourceResponse
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class UserResourcesResponse(UniversalBaseModel):
    data: typing.List[SingleUserResourceResponse]
    next: typing.Optional[str] = None
    next_cursor: typing.Optional[str] = pydantic.Field(default=None)
    """
    The cursor for fetching the next page, or `null` to fetch the first page.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
