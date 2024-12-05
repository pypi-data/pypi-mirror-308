# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
from .sleep_type import SleepType
import typing
from .sleep_summary_state import SleepSummaryState
from .client_facing_source import ClientFacingSource
from .client_facing_sleep_stream import ClientFacingSleepStream
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class ClientFacingSleep(UniversalBaseModel):
    user_id: str = pydantic.Field()
    """
    User id returned by vital create user request. This id should be stored in your database against the user and used for all interactions with the vital api.
    """

    id: str
    date: str = pydantic.Field()
    """
    Date of the specified record, formatted as ISO8601 datetime string in UTC 00:00. Deprecated in favour of calendar_date.
    """

    calendar_date: str = pydantic.Field()
    """
    Date of the sleep summary in the YYYY-mm-dd format. This generally matches the sleep end date.
    """

    bedtime_start: str = pydantic.Field()
    """
    UTC Time when the sleep period started
    """

    bedtime_stop: str = pydantic.Field()
    """
    UTC Time when the sleep period ended
    """

    type: SleepType = pydantic.Field()
    """
    `long_sleep`: >=3 hours of sleep;
    `short_sleep`: <3 hours of sleep;
    `acknowledged_nap`: User-acknowledged naps, typically under 3 hours of sleep;
    `unknown`: The sleep session recording is ongoing.
    """

    timezone_offset: typing.Optional[int] = pydantic.Field(default=None)
    """
    Timezone offset from UTC as seconds. For example, EEST (Eastern European Summer Time, +3h) is 10800. PST (Pacific Standard Time, -8h) is -28800::seconds
    """

    duration: int = pydantic.Field()
    """
    Total duration of the sleep period (sleep.duration = sleep.bedtime_end - sleep.bedtime_start)::seconds
    """

    total: int = pydantic.Field()
    """
    Total amount of sleep registered during the sleep period (sleep.total = sleep.rem + sleep.light + sleep.deep)::seconds
    """

    awake: int = pydantic.Field()
    """
    Total amount of awake time registered during the sleep period::seconds
    """

    light: int = pydantic.Field()
    """
    Total amount of light sleep registered during the sleep period::seconds
    """

    rem: int = pydantic.Field()
    """
    Total amount of REM sleep registered during the sleep period, minutes::seconds
    """

    deep: int = pydantic.Field()
    """
    Total amount of deep (N3) sleep registered during the sleep period::seconds
    """

    score: typing.Optional[int] = pydantic.Field(default=None)
    """
    A value between 1 and 100 representing how well the user slept. Currently only available for Withings, Oura, Whoop and Garmin::scalar
    """

    hr_lowest: typing.Optional[int] = pydantic.Field(default=None)
    """
    The lowest heart rate (5 minutes sliding average) registered during the sleep period::beats per minute
    """

    hr_average: typing.Optional[int] = pydantic.Field(default=None)
    """
    The average heart rate registered during the sleep period::beats per minute
    """

    efficiency: typing.Optional[float] = pydantic.Field(default=None)
    """
    Sleep efficiency is the percentage of the sleep period spent asleep (100% \* sleep.total / sleep.duration)::perc
    """

    latency: typing.Optional[int] = pydantic.Field(default=None)
    """
    Detected latency from bedtime_start to the beginning of the first five minutes of persistent sleep::seconds
    """

    temperature_delta: typing.Optional[float] = pydantic.Field(default=None)
    """
    Skin temperature deviation from the long-term temperature average::celcius
    """

    skin_temperature: typing.Optional[float] = pydantic.Field(default=None)
    """
    The skin temperature::celcius
    """

    hr_dip: typing.Optional[float] = pydantic.Field(default=None)
    """
    Sleeping Heart Rate Dip is the percentage difference between your average waking heart rate and your average sleeping heart rate. In health studies, a greater "dip" is typically seen as a positive indicator of overall health. Currently only available for Garmin::perc
    """

    state: typing.Optional[SleepSummaryState] = pydantic.Field(default=None)
    """
    Some providers can provide updates to the sleep summary hours after the sleep period has ended. This field indicates the state of the sleep summary. For example, TENTATIVE means the summary is an intial prediction from the provider and can be subject to change. Currently only available for Garmin and EightSleep::str
    """

    average_hrv: typing.Optional[float] = pydantic.Field(default=None)
    """
    The average heart rate variability registered during the sleep period::rmssd
    """

    respiratory_rate: typing.Optional[float] = pydantic.Field(default=None)
    """
    Average respiratory rate::breaths per minute
    """

    source: ClientFacingSource = pydantic.Field()
    """
    Source the data has come from.
    """

    sleep_stream: typing.Optional[ClientFacingSleepStream] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
