# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "ScoringFnDefWithProviderParam",
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


class ParameterTypePtString(TypedDict, total=False):
    type: Required[Literal["string"]]


class ParameterTypePtNumber(TypedDict, total=False):
    type: Required[Literal["number"]]


class ParameterTypePtBoolean(TypedDict, total=False):
    type: Required[Literal["boolean"]]


class ParameterTypePtArray(TypedDict, total=False):
    type: Required[Literal["array"]]


class ParameterTypePtObject(TypedDict, total=False):
    type: Required[Literal["object"]]


class ParameterTypePtJson(TypedDict, total=False):
    type: Required[Literal["json"]]


class ParameterTypePtUnion(TypedDict, total=False):
    type: Required[Literal["union"]]


class ParameterTypePtChatCompletionInput(TypedDict, total=False):
    type: Required[Literal["chat_completion_input"]]


class ParameterTypePtCompletionInput(TypedDict, total=False):
    type: Required[Literal["completion_input"]]


class ParameterTypePtAgentTurnInput(TypedDict, total=False):
    type: Required[Literal["agent_turn_input"]]


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


class Parameter(TypedDict, total=False):
    name: Required[str]

    type: Required[ParameterType]

    description: str


class ReturnTypeRtString(TypedDict, total=False):
    type: Required[Literal["string"]]


class ReturnTypeRtNumber(TypedDict, total=False):
    type: Required[Literal["number"]]


class ReturnTypeRtBoolean(TypedDict, total=False):
    type: Required[Literal["boolean"]]


class ReturnTypeRtArray(TypedDict, total=False):
    type: Required[Literal["array"]]


class ReturnTypeRtObject(TypedDict, total=False):
    type: Required[Literal["object"]]


class ReturnTypeRtJson(TypedDict, total=False):
    type: Required[Literal["json"]]


class ReturnTypeRtUnion(TypedDict, total=False):
    type: Required[Literal["union"]]


class ReturnTypeRtChatCompletionInput(TypedDict, total=False):
    type: Required[Literal["chat_completion_input"]]


class ReturnTypeRtCompletionInput(TypedDict, total=False):
    type: Required[Literal["completion_input"]]


class ReturnTypeRtAgentTurnInput(TypedDict, total=False):
    type: Required[Literal["agent_turn_input"]]


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


class Context(TypedDict, total=False):
    judge_model: Required[str]

    judge_score_regex: List[str]

    prompt_template: str


class ScoringFnDefWithProviderParam(TypedDict, total=False):
    identifier: Required[str]

    metadata: Required[Dict[str, Union[bool, float, str, Iterable[object], object, None]]]

    parameters: Required[Iterable[Parameter]]

    provider_id: Required[str]

    return_type: Required[ReturnType]

    context: Context

    description: str
