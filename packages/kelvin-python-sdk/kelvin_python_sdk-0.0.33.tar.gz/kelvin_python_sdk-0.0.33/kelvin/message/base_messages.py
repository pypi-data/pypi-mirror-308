from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, validator
from typing_extensions import Literal

from kelvin.krn import KRN, KRNAsset
from kelvin.message.message import Message
from kelvin.message.msg_type import (
    KMessageTypeControl,
    KMessageTypeControlAck,
    KMessageTypeControlStatus,
    KMessageTypeData,
    KMessageTypeDataTag,
    KMessageTypeParameters,
    KMessageTypeRecommendation,
    KMessageTypeRuntimeManifest,
)
from kelvin.message.utils import from_rfc3339_timestamp, to_rfc3339_timestamp


class ValuePoint(BaseModel):
    value: Any
    timestamp: datetime
    source: Optional[str]


class ControlChangePayload(BaseModel):
    timeout: Optional[int] = Field(description="Timeout for retries")
    retries: Optional[int] = Field(description="Max retries")
    expiration_date: datetime = Field(description="Absolute expiration Date in UTC")
    payload: Any = Field(None, description="Control Change payload")

    from_value: Optional[ValuePoint] = Field(
        None, description="Optional value of the datastream at the moment of the creation", alias="from"
    )

    class Config:
        json_encoders = {datetime: to_rfc3339_timestamp}
        allow_population_by_field_name = True

    @validator("expiration_date", pre=True, always=True)
    def parse_expiration_date(cls, v: Union[str, datetime]) -> datetime:
        if isinstance(v, str):
            return from_rfc3339_timestamp(v)
        return v


class ControlChangeMsg(Message):
    """Generic Control Change Message"""

    _TYPE = KMessageTypeControl()

    payload: ControlChangePayload


class StateEnum(str, Enum):
    ready = "ready"
    sent = "sent"
    failed = "failed"
    processed = "processed"
    applied = "applied"
    rejected = "rejected"


class ReportedValues(BaseModel):
    before: Optional[ValuePoint]
    after: Optional[ValuePoint]


class ControlChangeStatusPayload(BaseModel):
    state: StateEnum
    message: Optional[str] = None
    reported: Optional[ReportedValues] = None

    # not used anymore, kept to avoid breaks
    payload: Optional[Any] = Field(None, description="Metric value at status time")


class ControlChangeStatus(Message):
    """Control Change Status"""

    _TYPE = KMessageTypeControlStatus()

    payload: ControlChangeStatusPayload


class ControlChangeAck(Message):
    """Control Change Ack"""

    _TYPE = KMessageTypeControlAck()

    payload: ControlChangeStatusPayload


class SensorDataPayload(BaseModel):
    data: List[float] = Field(..., description="Array of sensor measurements.", min_items=1)
    sample_rate: float = Field(..., description="Sensor sample-rate in Hertz.", gt=0.0)


class SensorDataMsg(Message):
    """Sensor data."""

    _TYPE = KMessageTypeData("object", "kelvin.sensor_data")

    payload: SensorDataPayload


class RecommendationControlChange(ControlChangePayload):
    retries: Optional[int] = Field(description="Max retries", alias="retry")
    state: Optional[str]
    resource: Optional[KRN]
    control_change_id: Optional[UUID] = Field(description="Control Change ID")


class RecommendationActions(BaseModel):
    control_changes: List[RecommendationControlChange] = []


class RecommendationPayload(BaseModel):
    source: Optional[KRN]
    resource: KRN
    type: str
    description: Optional[str]
    confidence: Optional[int] = Field(ge=1, le=4)
    expiration_date: Optional[datetime]
    actions: RecommendationActions = RecommendationActions()
    metadata: Dict[str, Any] = {}
    state: Optional[Literal["pending", "auto_accepted"]]

    class Config:
        json_encoders = {datetime: to_rfc3339_timestamp}

    @validator("expiration_date", pre=True, always=True)
    def parse_expiration_date(cls, v: Union[str, datetime]) -> datetime:
        if isinstance(v, str):
            return from_rfc3339_timestamp(v)
        return v


class RecommendationMsg(Message):
    _TYPE = KMessageTypeRecommendation()

    payload: RecommendationPayload


class EdgeParameter(BaseModel):
    name: str
    value: Union[StrictBool, StrictInt, StrictFloat, StrictStr]
    comment: Optional[str]


class ResourceParameters(BaseModel):
    resource: KRN
    parameters: List[EdgeParameter]


class ParametersPayload(BaseModel):
    source: Optional[KRN]
    resource_parameters: List[ResourceParameters]


class ParametersMsg(Message):
    _TYPE = KMessageTypeParameters()

    payload: ParametersPayload


class ManifestDatastream(BaseModel):
    class Config:
        extra = "allow"

    name: str
    primitive_type_name: Optional[str]
    data_type_name: Optional[str]
    semantic_type_name: Optional[str]
    unit_name: Optional[str]


class ResourceDatastream(BaseModel):
    map_to: Optional[str]
    remote: Optional[bool]
    access: Literal["RO", "RW", "WO"] = "RO"
    owned: Optional[bool] = False
    configuration: Dict = {}


class Resource(BaseModel):
    type: str = ""
    name: str = ""
    properties: Dict[str, Union[StrictBool, StrictInt, StrictFloat, StrictStr]] = {}
    parameters: Dict[str, Union[StrictBool, StrictInt, StrictFloat, StrictStr]] = {}
    datastreams: Dict[str, ResourceDatastream] = {}


class RuntimeManifestPayload(BaseModel):
    resources: List[Resource] = []
    configuration: Dict = {}
    datastreams: List[ManifestDatastream] = []


class RuntimeManifest(Message):
    _TYPE = KMessageTypeRuntimeManifest()

    payload: RuntimeManifestPayload


class DataTagPayload(BaseModel):
    start_date: datetime
    end_date: datetime
    tag_name: str
    resource: KRNAsset
    description: Optional[str] = Field(None, max_length=256)
    contexts: Optional[List[KRN]] = None
    source: Optional[KRN]


class DataTagMsg(Message):
    _TYPE = KMessageTypeDataTag()

    resource: KRNAsset
    payload: DataTagPayload
