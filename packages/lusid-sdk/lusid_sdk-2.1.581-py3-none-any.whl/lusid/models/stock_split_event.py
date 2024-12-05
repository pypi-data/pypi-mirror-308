# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import Any, Dict, Optional, Union
from pydantic.v1 import Field, StrictFloat, StrictInt, StrictStr, validator
from lusid.models.instrument_event import InstrumentEvent
from lusid.models.units_ratio import UnitsRatio

class StockSplitEvent(InstrumentEvent):
    """
    A split in the company's shares. Shareholders are given additional company shares based on the terms of the stock split.  # noqa: E501
    """
    payment_date: datetime = Field(..., alias="paymentDate", description="Date on which the stock split takes effect.")
    ex_date: datetime = Field(..., alias="exDate", description="The first date on which the shares will trade at the post-split price.")
    units_ratio: UnitsRatio = Field(..., alias="unitsRatio")
    record_date: Optional[datetime] = Field(None, alias="recordDate", description="Date you have to be the holder of record in order to receive the additional shares.")
    announcement_date: Optional[datetime] = Field(None, alias="announcementDate", description="Date the stock split was announced.")
    fractional_units_cash_price: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="fractionalUnitsCashPrice", description="The cash price per unit paid in lieu when fractional units can not be distributed.")
    fractional_units_cash_currency: Optional[StrictStr] = Field(None, alias="fractionalUnitsCashCurrency", description="The currency of the cash paid in lieu of fractional units.")
    instrument_event_type: StrictStr = Field(..., alias="instrumentEventType", description="The Type of Event. The available values are: TransitionEvent, InformationalEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent, AmortisationEvent, CashFlowEvent, ExerciseEvent, ResetEvent, TriggerEvent, RawVendorEvent, InformationalErrorEvent, BondCouponEvent, DividendReinvestmentEvent, AccumulationEvent, BondPrincipalEvent, DividendOptionEvent, MaturityEvent, FxForwardSettlementEvent, ExpiryEvent, ScripDividendEvent, StockDividendEvent, ReverseStockSplitEvent, CapitalDistributionEvent, SpinOffEvent, MergerEvent, FutureExpiryEvent, SwapCashFlowEvent, SwapPrincipalEvent, CreditPremiumCashFlowEvent, CdsCreditEvent, CdxCreditEvent, MbsCouponEvent, MbsPrincipalEvent, BonusIssueEvent, MbsPrincipalWriteOffEvent, MbsInterestDeferralEvent, MbsInterestShortfallEvent, TenderEvent, CallOnIntermediateSecuritiesEvent, IntermediateSecuritiesDistributionEvent, OptionExercisePhysicalEvent, OptionExerciseCashEvent, ProtectionPayoutCashFlowEvent, TermDepositInterestEvent, TermDepositPrincipalEvent")
    additional_properties: Dict[str, Any] = {}
    __properties = ["instrumentEventType", "paymentDate", "exDate", "unitsRatio", "recordDate", "announcementDate", "fractionalUnitsCashPrice", "fractionalUnitsCashCurrency"]

    @validator('instrument_event_type')
    def instrument_event_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('TransitionEvent', 'InformationalEvent', 'OpenEvent', 'CloseEvent', 'StockSplitEvent', 'BondDefaultEvent', 'CashDividendEvent', 'AmortisationEvent', 'CashFlowEvent', 'ExerciseEvent', 'ResetEvent', 'TriggerEvent', 'RawVendorEvent', 'InformationalErrorEvent', 'BondCouponEvent', 'DividendReinvestmentEvent', 'AccumulationEvent', 'BondPrincipalEvent', 'DividendOptionEvent', 'MaturityEvent', 'FxForwardSettlementEvent', 'ExpiryEvent', 'ScripDividendEvent', 'StockDividendEvent', 'ReverseStockSplitEvent', 'CapitalDistributionEvent', 'SpinOffEvent', 'MergerEvent', 'FutureExpiryEvent', 'SwapCashFlowEvent', 'SwapPrincipalEvent', 'CreditPremiumCashFlowEvent', 'CdsCreditEvent', 'CdxCreditEvent', 'MbsCouponEvent', 'MbsPrincipalEvent', 'BonusIssueEvent', 'MbsPrincipalWriteOffEvent', 'MbsInterestDeferralEvent', 'MbsInterestShortfallEvent', 'TenderEvent', 'CallOnIntermediateSecuritiesEvent', 'IntermediateSecuritiesDistributionEvent', 'OptionExercisePhysicalEvent', 'OptionExerciseCashEvent', 'ProtectionPayoutCashFlowEvent', 'TermDepositInterestEvent', 'TermDepositPrincipalEvent'):
            raise ValueError("must be one of enum values ('TransitionEvent', 'InformationalEvent', 'OpenEvent', 'CloseEvent', 'StockSplitEvent', 'BondDefaultEvent', 'CashDividendEvent', 'AmortisationEvent', 'CashFlowEvent', 'ExerciseEvent', 'ResetEvent', 'TriggerEvent', 'RawVendorEvent', 'InformationalErrorEvent', 'BondCouponEvent', 'DividendReinvestmentEvent', 'AccumulationEvent', 'BondPrincipalEvent', 'DividendOptionEvent', 'MaturityEvent', 'FxForwardSettlementEvent', 'ExpiryEvent', 'ScripDividendEvent', 'StockDividendEvent', 'ReverseStockSplitEvent', 'CapitalDistributionEvent', 'SpinOffEvent', 'MergerEvent', 'FutureExpiryEvent', 'SwapCashFlowEvent', 'SwapPrincipalEvent', 'CreditPremiumCashFlowEvent', 'CdsCreditEvent', 'CdxCreditEvent', 'MbsCouponEvent', 'MbsPrincipalEvent', 'BonusIssueEvent', 'MbsPrincipalWriteOffEvent', 'MbsInterestDeferralEvent', 'MbsInterestShortfallEvent', 'TenderEvent', 'CallOnIntermediateSecuritiesEvent', 'IntermediateSecuritiesDistributionEvent', 'OptionExercisePhysicalEvent', 'OptionExerciseCashEvent', 'ProtectionPayoutCashFlowEvent', 'TermDepositInterestEvent', 'TermDepositPrincipalEvent')")
        return value

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> StockSplitEvent:
        """Create an instance of StockSplitEvent from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of units_ratio
        if self.units_ratio:
            _dict['unitsRatio'] = self.units_ratio.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        # set to None if record_date (nullable) is None
        # and __fields_set__ contains the field
        if self.record_date is None and "record_date" in self.__fields_set__:
            _dict['recordDate'] = None

        # set to None if announcement_date (nullable) is None
        # and __fields_set__ contains the field
        if self.announcement_date is None and "announcement_date" in self.__fields_set__:
            _dict['announcementDate'] = None

        # set to None if fractional_units_cash_price (nullable) is None
        # and __fields_set__ contains the field
        if self.fractional_units_cash_price is None and "fractional_units_cash_price" in self.__fields_set__:
            _dict['fractionalUnitsCashPrice'] = None

        # set to None if fractional_units_cash_currency (nullable) is None
        # and __fields_set__ contains the field
        if self.fractional_units_cash_currency is None and "fractional_units_cash_currency" in self.__fields_set__:
            _dict['fractionalUnitsCashCurrency'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> StockSplitEvent:
        """Create an instance of StockSplitEvent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StockSplitEvent.parse_obj(obj)

        _obj = StockSplitEvent.parse_obj({
            "instrument_event_type": obj.get("instrumentEventType"),
            "payment_date": obj.get("paymentDate"),
            "ex_date": obj.get("exDate"),
            "units_ratio": UnitsRatio.from_dict(obj.get("unitsRatio")) if obj.get("unitsRatio") is not None else None,
            "record_date": obj.get("recordDate"),
            "announcement_date": obj.get("announcementDate"),
            "fractional_units_cash_price": obj.get("fractionalUnitsCashPrice"),
            "fractional_units_cash_currency": obj.get("fractionalUnitsCashCurrency")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
