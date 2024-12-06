import datetime
from typing import Optional

import classifications as classif
import pandas as pd
from pydantic import Field, PrivateAttr

import dataio.schemas.bonsai_api.PPF_fact_schemas as PPF_fact_schemas
from dataio.schemas.bonsai_api.base_models import FactBaseModel
from typing import Dict, ClassVar

class baseExternalSchemas(FactBaseModel):
    # Created with Sanders. Might Not be the base
    location: str
    time: int
    unit: str
    value: float
    comment: Optional[str] = None
    flag: Optional[str] = None


class ExternalMonetarySUT(baseExternalSchemas):
    table_type: str  # Supply or use table
    product_code: str
    product_name: str
    activity_code: str
    activity_name: str
    price_type: str = Field(  # Current price or previous year price.
        default="current prices"
    )
    consumer_price: bool = Field(default=False)  # Consumer price vs production price
    money_unit: Optional[str] = None  # Millions, billions etc.


# for tables with annual data that start on a day other than January 1st. For example for the fiscal year of India.
class BrokenYearMonetarySUT(ExternalMonetarySUT):
    time: datetime.date  # Start date of fiscal year


class PRODCOMProductionVolume(PPF_fact_schemas.ProductionVolumes):
    indicator: str

    _classification: ClassVar[Dict[str, str]] = {
        "location": "prodcom",
        "product": "prodcom_total_2_0",  # could also be prodcom_sold_2_0 depending on context
    }

    def __str__(self) -> str:
        return f"{self.location}-{self.product}-{self.activity}-{self.time}-{self.value}-{self.unit}"


class IndustrialCommodityStatistic(PPF_fact_schemas.ProductionVolumes):

    def __str__(self) -> str:
        return f"{self.location}-{self.product}-{self.activity}-{self.time}-{self.value}-{self.unit}"


class UNdataEnergyBalance(FactBaseModel):
    activity: str
    product: str
    location: str
    time: int
    value: float
    unit: str
    comment: Optional[str] = None
    flag: Optional[str] = None

    _classification: ClassVar[Dict[str, str]] = {
        "location": "undata_energy",
        "product": "undata_energy_stats", #or prodcom_sold_2_0
    }


    def __str__(self) -> str:
        return f"{self.location}-{self.product}-{self.activity}-{self.time}"

class UNdataEnergyStatistic(FactBaseModel):
    activity: str
    product: str
    location: str
    time: int
    value: float
    unit: str
    comment: Optional[str] = None
    flag: Optional[str] = None
    conversion_factor: Optional[float] = None

    _classification: ClassVar[Dict[str, str]] = {
        "location": "undata_energy",
        "product": "undata_energy_stats",
        "activity": "undata_energy_stats"
    }

    def __str__(self) -> str:
        return f"{self.location}-{self.product}-{self.activity}-{self.time}"


class BACITrade(FactBaseModel):
    time: int
    HS07: int
    country_exp: str
    country_imp: str
    value: float
    unit: str
    flag: Optional[str] = None

    _classification: ClassVar[Dict[str, str]] = {
        "location": "baci",
        "product": "baci",
    }

class USGSProductionVolume(PPF_fact_schemas.ProductionVolumes):

    _classification: ClassVar[Dict[str, str]] = {
        "location": "undata_energy",
        "product": "undata_energy_stats",
    }

    def __str__(self) -> str:
        return f"{self.location}-{self.product}-{self.activity}-{self.time}-{self.value}-{self.unit}"
