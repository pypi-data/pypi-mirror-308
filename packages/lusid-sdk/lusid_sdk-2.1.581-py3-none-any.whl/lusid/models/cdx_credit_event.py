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

class CdxCreditEvent(InstrumentEvent):
    """
    Definition of a credit event for credit default swap index (CDX) instruments.  # noqa: E501
    """
    effective_date: datetime = Field(..., alias="effectiveDate", description="The date of the credit default - i.e. date on which the debt issuer defaulted on its repayment obligation.")
    auction_date: Optional[datetime] = Field(None, alias="auctionDate", description="The date of the credit event auction - i.e. date on which the defaulted debt is sold via auction, and a recovery rate determined.")
    recovery_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="recoveryRate", description="The fraction of the defaulted debt that can be recovered.")
    constituent_weight: Union[StrictFloat, StrictInt] = Field(..., alias="constituentWeight", description="The relative weight of the CDX constituent.")
    constituent_reference: Optional[StrictStr] = Field(None, alias="constituentReference", description="Reference value used to identify the CDX constituent.")
    instrument_event_type: StrictStr = Field(..., alias="instrumentEventType", description="The Type of Event. The available values are: TransitionEvent, InformationalEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent, AmortisationEvent, CashFlowEvent, ExerciseEvent, ResetEvent, TriggerEvent, RawVendorEvent, InformationalErrorEvent, BondCouponEvent, DividendReinvestmentEvent, AccumulationEvent, BondPrincipalEvent, DividendOptionEvent, MaturityEvent, FxForwardSettlementEvent, ExpiryEvent, ScripDividendEvent, StockDividendEvent, ReverseStockSplitEvent, CapitalDistributionEvent, SpinOffEvent, MergerEvent, FutureExpiryEvent, SwapCashFlowEvent, SwapPrincipalEvent, CreditPremiumCashFlowEvent, CdsCreditEvent, CdxCreditEvent, MbsCouponEvent, MbsPrincipalEvent, BonusIssueEvent, MbsPrincipalWriteOffEvent, MbsInterestDeferralEvent, MbsInterestShortfallEvent, TenderEvent, CallOnIntermediateSecuritiesEvent, IntermediateSecuritiesDistributionEvent, OptionExercisePhysicalEvent, OptionExerciseCashEvent, ProtectionPayoutCashFlowEvent, TermDepositInterestEvent, TermDepositPrincipalEvent")
    additional_properties: Dict[str, Any] = {}
    __properties = ["instrumentEventType", "effectiveDate", "auctionDate", "recoveryRate", "constituentWeight", "constituentReference"]

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
    def from_json(cls, json_str: str) -> CdxCreditEvent:
        """Create an instance of CdxCreditEvent from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        # set to None if auction_date (nullable) is None
        # and __fields_set__ contains the field
        if self.auction_date is None and "auction_date" in self.__fields_set__:
            _dict['auctionDate'] = None

        # set to None if recovery_rate (nullable) is None
        # and __fields_set__ contains the field
        if self.recovery_rate is None and "recovery_rate" in self.__fields_set__:
            _dict['recoveryRate'] = None

        # set to None if constituent_reference (nullable) is None
        # and __fields_set__ contains the field
        if self.constituent_reference is None and "constituent_reference" in self.__fields_set__:
            _dict['constituentReference'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CdxCreditEvent:
        """Create an instance of CdxCreditEvent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CdxCreditEvent.parse_obj(obj)

        _obj = CdxCreditEvent.parse_obj({
            "instrument_event_type": obj.get("instrumentEventType"),
            "effective_date": obj.get("effectiveDate"),
            "auction_date": obj.get("auctionDate"),
            "recovery_rate": obj.get("recoveryRate"),
            "constituent_weight": obj.get("constituentWeight"),
            "constituent_reference": obj.get("constituentReference")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
