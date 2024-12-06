# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "ScoringFnDefWithProvider",
    "Parameter",
    "ParameterType",
    "ParameterTypePtString",
    "ParameterTypePtNumber",
    "ParameterTypePtBoolean",
    "ParameterTypePtArray",
    "ParameterTypePtObject",
    "ParameterTypePtJson",
    "ParameterTypePtUnion",
    "ParameterTypePtChatCompletionInput",
    "ParameterTypePtCompletionInput",
    "ParameterTypePtAgentTurnInput",
    "ReturnType",
    "ReturnTypeRtString",
    "ReturnTypeRtNumber",
    "ReturnTypeRtBoolean",
    "ReturnTypeRtArray",
    "ReturnTypeRtObject",
    "ReturnTypeRtJson",
    "ReturnTypeRtUnion",
    "ReturnTypeRtChatCompletionInput",
    "ReturnTypeRtCompletionInput",
    "ReturnTypeRtAgentTurnInput",
    "Context",
]


class ParameterTypePtString(BaseModel):
    type: Literal["string"]


class ParameterTypePtNumber(BaseModel):
    type: Literal["number"]


class ParameterTypePtBoolean(BaseModel):
    type: Literal["boolean"]


class ParameterTypePtArray(BaseModel):
    type: Literal["array"]


class ParameterTypePtObject(BaseModel):
    type: Literal["object"]


class ParameterTypePtJson(BaseModel):
    type: Literal["json"]


class ParameterTypePtUnion(BaseModel):
    type: Literal["union"]


class ParameterTypePtChatCompletionInput(BaseModel):
    type: Literal["chat_completion_input"]


class ParameterTypePtCompletionInput(BaseModel):
    type: Literal["completion_input"]


class ParameterTypePtAgentTurnInput(BaseModel):
    type: Literal["agent_turn_input"]


ParameterType: TypeAlias = Union[
    ParameterTypePtString,
    ParameterTypePtNumber,
    ParameterTypePtBoolean,
    ParameterTypePtArray,
    ParameterTypePtObject,
    ParameterTypePtJson,
    ParameterTypePtUnion,
    ParameterTypePtChatCompletionInput,
    ParameterTypePtCompletionInput,
    ParameterTypePtAgentTurnInput,
]


class Parameter(BaseModel):
    name: str

    type: ParameterType

    description: Optional[str] = None


class ReturnTypeRtString(BaseModel):
    type: Literal["string"]


class ReturnTypeRtNumber(BaseModel):
    type: Literal["number"]


class ReturnTypeRtBoolean(BaseModel):
    type: Literal["boolean"]


class ReturnTypeRtArray(BaseModel):
    type: Literal["array"]


class ReturnTypeRtObject(BaseModel):
    type: Literal["object"]


class ReturnTypeRtJson(BaseModel):
    type: Literal["json"]


class ReturnTypeRtUnion(BaseModel):
    type: Literal["union"]


class ReturnTypeRtChatCompletionInput(BaseModel):
    type: Literal["chat_completion_input"]


class ReturnTypeRtCompletionInput(BaseModel):
    type: Literal["completion_input"]


class ReturnTypeRtAgentTurnInput(BaseModel):
    type: Literal["agent_turn_input"]


ReturnType: TypeAlias = Union[
    ReturnTypeRtString,
    ReturnTypeRtNumber,
    ReturnTypeRtBoolean,
    ReturnTypeRtArray,
    ReturnTypeRtObject,
    ReturnTypeRtJson,
    ReturnTypeRtUnion,
    ReturnTypeRtChatCompletionInput,
    ReturnTypeRtCompletionInput,
    ReturnTypeRtAgentTurnInput,
]


class Context(BaseModel):
    judge_model: str

    judge_score_regex: Optional[List[str]] = None

    prompt_template: Optional[str] = None


class ScoringFnDefWithProvider(BaseModel):
    identifier: str

    metadata: Dict[str, Union[bool, float, str, List[object], object, None]]

    parameters: List[Parameter]

    provider_id: str

    return_type: ReturnType

    context: Optional[Context] = None

    description: Optional[str] = None
