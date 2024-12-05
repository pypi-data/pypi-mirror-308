# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .menstrual_flow_entry import MenstrualFlowEntry
from .cervical_mucus_entry import CervicalMucusEntry
from .intermenstrual_bleeding_entry import IntermenstrualBleedingEntry
from .contraceptive_entry import ContraceptiveEntry
from .detected_deviation_entry import DetectedDeviationEntry
from .ovulation_test_entry import OvulationTestEntry
from .home_pregnancy_test_entry import HomePregnancyTestEntry
from .home_progesterone_test_entry import HomeProgesteroneTestEntry
from .sexual_activity_entry import SexualActivityEntry
from .basal_body_temperature_entry import BasalBodyTemperatureEntry
from .client_facing_source import ClientFacingSource
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class MenstrualCycle(UniversalBaseModel):
    period_start: str
    period_end: typing.Optional[str] = None
    cycle_end: typing.Optional[str] = None
    is_predicted: typing.Optional[bool] = None
    menstrual_flow: typing.Optional[typing.List[MenstrualFlowEntry]] = None
    cervical_mucus: typing.Optional[typing.List[CervicalMucusEntry]] = None
    intermenstrual_bleeding: typing.Optional[typing.List[IntermenstrualBleedingEntry]] = None
    contraceptive: typing.Optional[typing.List[ContraceptiveEntry]] = None
    detected_deviations: typing.Optional[typing.List[DetectedDeviationEntry]] = None
    ovulation_test: typing.Optional[typing.List[OvulationTestEntry]] = None
    home_pregnancy_test: typing.Optional[typing.List[HomePregnancyTestEntry]] = None
    home_progesterone_test: typing.Optional[typing.List[HomeProgesteroneTestEntry]] = None
    sexual_activity: typing.Optional[typing.List[SexualActivityEntry]] = None
    basal_body_temperature: typing.Optional[typing.List[BasalBodyTemperatureEntry]] = None
    source: ClientFacingSource

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
