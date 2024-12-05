# This file was auto-generated by Fern from our API Definition.

from ..core.client_wrapper import SyncClientWrapper
import typing
from ..core.request_options import RequestOptions
from ..types.client_sleep_cycle_response import ClientSleepCycleResponse
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import parse_obj_as
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper


class SleepCycleClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self,
        user_id: str,
        *,
        start_date: str,
        end_date: typing.Optional[str] = None,
        provider: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ClientSleepCycleResponse:
        """
        Get Daily sleep cycle for user_id

        Parameters
        ----------
        user_id : str

        start_date : str

        end_date : typing.Optional[str]

        provider : typing.Optional[str]
            Provider oura/strava etc

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ClientSleepCycleResponse
            Successful Response

        Examples
        --------
        from vital import Vital

        client = Vital(
            api_key="YOUR_API_KEY",
        )
        client.sleep_cycle.get(
            user_id="user_id",
            start_date="start_date",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/summary/sleep_cycle/{jsonable_encoder(user_id)}",
            method="GET",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "provider": provider,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ClientSleepCycleResponse,
                    parse_obj_as(
                        type_=ClientSleepCycleResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncSleepCycleClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get(
        self,
        user_id: str,
        *,
        start_date: str,
        end_date: typing.Optional[str] = None,
        provider: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ClientSleepCycleResponse:
        """
        Get Daily sleep cycle for user_id

        Parameters
        ----------
        user_id : str

        start_date : str

        end_date : typing.Optional[str]

        provider : typing.Optional[str]
            Provider oura/strava etc

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ClientSleepCycleResponse
            Successful Response

        Examples
        --------
        import asyncio

        from vital import AsyncVital

        client = AsyncVital(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.sleep_cycle.get(
                user_id="user_id",
                start_date="start_date",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/summary/sleep_cycle/{jsonable_encoder(user_id)}",
            method="GET",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "provider": provider,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ClientSleepCycleResponse,
                    parse_obj_as(
                        type_=ClientSleepCycleResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
