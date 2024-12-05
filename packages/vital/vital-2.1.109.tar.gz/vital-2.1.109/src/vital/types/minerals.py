# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class Minerals(str, enum.Enum):
    SODIUM = "sodium"
    POTASSIUM = "potassium"
    CALCIUM = "calcium"
    PHOSPHORUS = "phosphorus"
    MAGNESIUM = "magnesium"
    IRON = "iron"
    ZINC = "zinc"
    FLUORIDE = "fluoride"
    CHLORIDE = "chloride"
    BORON = "boron"
    COBALT = "cobalt"
    NICKEL = "nickel"
    SILICON = "silicon"
    VANADIUM = "vanadium"
    LITHIUM = "lithium"
    RUBIDIUM = "rubidium"
    STRONTIUM = "strontium"
    ALUMINUM = "aluminum"
    ARSENIC = "arsenic"
    BARIUM = "barium"
    BERYLLIUM = "beryllium"
    BISMUTH = "bismuth"
    CADMIUM = "cadmium"
    CESIUM = "cesium"
    GERMANIUM = "germanium"
    GOLD = "gold"
    LEAD = "lead"
    MERCURY = "mercury"
    PALLADIUM = "palladium"
    PLATINUM = "platinum"
    SILVER = "silver"
    THALLIUM = "thallium"
    THORIUM = "thorium"
    TIN = "tin"
    TITANIUM = "titanium"
    TUNGSTEN = "tungsten"
    URANIUM = "uranium"
    ZIRCONIUM = "zirconium"

    def visit(
        self,
        sodium: typing.Callable[[], T_Result],
        potassium: typing.Callable[[], T_Result],
        calcium: typing.Callable[[], T_Result],
        phosphorus: typing.Callable[[], T_Result],
        magnesium: typing.Callable[[], T_Result],
        iron: typing.Callable[[], T_Result],
        zinc: typing.Callable[[], T_Result],
        fluoride: typing.Callable[[], T_Result],
        chloride: typing.Callable[[], T_Result],
        boron: typing.Callable[[], T_Result],
        cobalt: typing.Callable[[], T_Result],
        nickel: typing.Callable[[], T_Result],
        silicon: typing.Callable[[], T_Result],
        vanadium: typing.Callable[[], T_Result],
        lithium: typing.Callable[[], T_Result],
        rubidium: typing.Callable[[], T_Result],
        strontium: typing.Callable[[], T_Result],
        aluminum: typing.Callable[[], T_Result],
        arsenic: typing.Callable[[], T_Result],
        barium: typing.Callable[[], T_Result],
        beryllium: typing.Callable[[], T_Result],
        bismuth: typing.Callable[[], T_Result],
        cadmium: typing.Callable[[], T_Result],
        cesium: typing.Callable[[], T_Result],
        germanium: typing.Callable[[], T_Result],
        gold: typing.Callable[[], T_Result],
        lead: typing.Callable[[], T_Result],
        mercury: typing.Callable[[], T_Result],
        palladium: typing.Callable[[], T_Result],
        platinum: typing.Callable[[], T_Result],
        silver: typing.Callable[[], T_Result],
        thallium: typing.Callable[[], T_Result],
        thorium: typing.Callable[[], T_Result],
        tin: typing.Callable[[], T_Result],
        titanium: typing.Callable[[], T_Result],
        tungsten: typing.Callable[[], T_Result],
        uranium: typing.Callable[[], T_Result],
        zirconium: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is Minerals.SODIUM:
            return sodium()
        if self is Minerals.POTASSIUM:
            return potassium()
        if self is Minerals.CALCIUM:
            return calcium()
        if self is Minerals.PHOSPHORUS:
            return phosphorus()
        if self is Minerals.MAGNESIUM:
            return magnesium()
        if self is Minerals.IRON:
            return iron()
        if self is Minerals.ZINC:
            return zinc()
        if self is Minerals.FLUORIDE:
            return fluoride()
        if self is Minerals.CHLORIDE:
            return chloride()
        if self is Minerals.BORON:
            return boron()
        if self is Minerals.COBALT:
            return cobalt()
        if self is Minerals.NICKEL:
            return nickel()
        if self is Minerals.SILICON:
            return silicon()
        if self is Minerals.VANADIUM:
            return vanadium()
        if self is Minerals.LITHIUM:
            return lithium()
        if self is Minerals.RUBIDIUM:
            return rubidium()
        if self is Minerals.STRONTIUM:
            return strontium()
        if self is Minerals.ALUMINUM:
            return aluminum()
        if self is Minerals.ARSENIC:
            return arsenic()
        if self is Minerals.BARIUM:
            return barium()
        if self is Minerals.BERYLLIUM:
            return beryllium()
        if self is Minerals.BISMUTH:
            return bismuth()
        if self is Minerals.CADMIUM:
            return cadmium()
        if self is Minerals.CESIUM:
            return cesium()
        if self is Minerals.GERMANIUM:
            return germanium()
        if self is Minerals.GOLD:
            return gold()
        if self is Minerals.LEAD:
            return lead()
        if self is Minerals.MERCURY:
            return mercury()
        if self is Minerals.PALLADIUM:
            return palladium()
        if self is Minerals.PLATINUM:
            return platinum()
        if self is Minerals.SILVER:
            return silver()
        if self is Minerals.THALLIUM:
            return thallium()
        if self is Minerals.THORIUM:
            return thorium()
        if self is Minerals.TIN:
            return tin()
        if self is Minerals.TITANIUM:
            return titanium()
        if self is Minerals.TUNGSTEN:
            return tungsten()
        if self is Minerals.URANIUM:
            return uranium()
        if self is Minerals.ZIRCONIUM:
            return zirconium()
