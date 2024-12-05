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
from typing import Any, Dict, List, Optional, Union
from pydantic.v1 import Field, StrictFloat, StrictInt, StrictStr, conlist, constr, validator
from lusid.models.instrument_event import InstrumentEvent
from lusid.models.option_exercise_election import OptionExerciseElection

class OptionExerciseCashEvent(InstrumentEvent):
    """
    Event for cash option exercises.  # noqa: E501
    """
    cash_flow_per_unit: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="cashFlowPerUnit", description="The cashflow per unit")
    exercise_date: Optional[datetime] = Field(None, alias="exerciseDate", description="The exercise date of the option.")
    delivery_date: Optional[datetime] = Field(None, alias="deliveryDate", description="The delivery date of the option.")
    exercise_type: constr(strict=True, min_length=1) = Field(..., alias="exerciseType", description="The optionality type of the underlying option e.g. American, European.    Supported string (enumeration) values are: [European, Bermudan, American].")
    maturity_date: datetime = Field(..., alias="maturityDate", description="The maturity date of the option.")
    moneyness: Optional[StrictStr] = Field(None, description="The moneyness of the option e.g. InTheMoney, OutOfTheMoney.    Supported string (enumeration) values are: [InTheMoney, OutOfTheMoney, AtTheMoney].")
    option_exercise_elections: Optional[conlist(OptionExerciseElection)] = Field(None, alias="optionExerciseElections", description="Option exercise election for this OptionExercisePhysicalEvent.")
    option_type: constr(strict=True, min_length=1) = Field(..., alias="optionType", description="Type of optionality that is present e.g. call, put.    Supported string (enumeration) values are: [Call, Put].")
    start_date: datetime = Field(..., alias="startDate", description="The start date of the option.")
    strike_currency: StrictStr = Field(..., alias="strikeCurrency", description="The strike currency of the equity option.")
    strike_per_unit: Union[StrictFloat, StrictInt] = Field(..., alias="strikePerUnit", description="The strike of the equity option times the number of shares to exchange if exercised.")
    underlying_value_per_unit: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="underlyingValuePerUnit", description="The underlying price times the number of shares to exchange if exercised.")
    instrument_event_type: StrictStr = Field(..., alias="instrumentEventType", description="The Type of Event. The available values are: TransitionEvent, InformationalEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent, AmortisationEvent, CashFlowEvent, ExerciseEvent, ResetEvent, TriggerEvent, RawVendorEvent, InformationalErrorEvent, BondCouponEvent, DividendReinvestmentEvent, AccumulationEvent, BondPrincipalEvent, DividendOptionEvent, MaturityEvent, FxForwardSettlementEvent, ExpiryEvent, ScripDividendEvent, StockDividendEvent, ReverseStockSplitEvent, CapitalDistributionEvent, SpinOffEvent, MergerEvent, FutureExpiryEvent, SwapCashFlowEvent, SwapPrincipalEvent, CreditPremiumCashFlowEvent, CdsCreditEvent, CdxCreditEvent, MbsCouponEvent, MbsPrincipalEvent, BonusIssueEvent, MbsPrincipalWriteOffEvent, MbsInterestDeferralEvent, MbsInterestShortfallEvent, TenderEvent, CallOnIntermediateSecuritiesEvent, IntermediateSecuritiesDistributionEvent, OptionExercisePhysicalEvent, OptionExerciseCashEvent, ProtectionPayoutCashFlowEvent, TermDepositInterestEvent, TermDepositPrincipalEvent")
    additional_properties: Dict[str, Any] = {}
    __properties = ["instrumentEventType", "cashFlowPerUnit", "exerciseDate", "deliveryDate", "exerciseType", "maturityDate", "moneyness", "optionExerciseElections", "optionType", "startDate", "strikeCurrency", "strikePerUnit", "underlyingValuePerUnit"]

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
    def from_json(cls, json_str: str) -> OptionExerciseCashEvent:
        """Create an instance of OptionExerciseCashEvent from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in option_exercise_elections (list)
        _items = []
        if self.option_exercise_elections:
            for _item in self.option_exercise_elections:
                if _item:
                    _items.append(_item.to_dict())
            _dict['optionExerciseElections'] = _items
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        # set to None if cash_flow_per_unit (nullable) is None
        # and __fields_set__ contains the field
        if self.cash_flow_per_unit is None and "cash_flow_per_unit" in self.__fields_set__:
            _dict['cashFlowPerUnit'] = None

        # set to None if exercise_date (nullable) is None
        # and __fields_set__ contains the field
        if self.exercise_date is None and "exercise_date" in self.__fields_set__:
            _dict['exerciseDate'] = None

        # set to None if delivery_date (nullable) is None
        # and __fields_set__ contains the field
        if self.delivery_date is None and "delivery_date" in self.__fields_set__:
            _dict['deliveryDate'] = None

        # set to None if moneyness (nullable) is None
        # and __fields_set__ contains the field
        if self.moneyness is None and "moneyness" in self.__fields_set__:
            _dict['moneyness'] = None

        # set to None if option_exercise_elections (nullable) is None
        # and __fields_set__ contains the field
        if self.option_exercise_elections is None and "option_exercise_elections" in self.__fields_set__:
            _dict['optionExerciseElections'] = None

        # set to None if underlying_value_per_unit (nullable) is None
        # and __fields_set__ contains the field
        if self.underlying_value_per_unit is None and "underlying_value_per_unit" in self.__fields_set__:
            _dict['underlyingValuePerUnit'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OptionExerciseCashEvent:
        """Create an instance of OptionExerciseCashEvent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OptionExerciseCashEvent.parse_obj(obj)

        _obj = OptionExerciseCashEvent.parse_obj({
            "instrument_event_type": obj.get("instrumentEventType"),
            "cash_flow_per_unit": obj.get("cashFlowPerUnit"),
            "exercise_date": obj.get("exerciseDate"),
            "delivery_date": obj.get("deliveryDate"),
            "exercise_type": obj.get("exerciseType"),
            "maturity_date": obj.get("maturityDate"),
            "moneyness": obj.get("moneyness"),
            "option_exercise_elections": [OptionExerciseElection.from_dict(_item) for _item in obj.get("optionExerciseElections")] if obj.get("optionExerciseElections") is not None else None,
            "option_type": obj.get("optionType"),
            "start_date": obj.get("startDate"),
            "strike_currency": obj.get("strikeCurrency"),
            "strike_per_unit": obj.get("strikePerUnit"),
            "underlying_value_per_unit": obj.get("underlyingValuePerUnit")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
