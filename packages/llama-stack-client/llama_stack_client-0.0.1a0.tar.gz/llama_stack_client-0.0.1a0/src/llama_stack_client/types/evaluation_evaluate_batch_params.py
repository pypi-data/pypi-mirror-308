# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .shared_params.agent_config import AgentConfig
from .shared_params.system_message import SystemMessage
from .shared_params.sampling_params import SamplingParams

__all__ = ["EvaluationEvaluateBatchParams", "Candidate", "CandidateModelCandidate", "CandidateAgentCandidate"]


class EvaluationEvaluateBatchParams(TypedDict, total=False):
    candidate: Required[Candidate]

    dataset_id: Required[str]

    scoring_functions: Required[List[str]]

    x_llama_stack_provider_data: Annotated[str, PropertyInfo(alias="X-LlamaStack-ProviderData")]


class CandidateModelCandidate(TypedDict, total=False):
    model: Required[str]

    sampling_params: Required[SamplingParams]

    type: Required[Literal["model"]]

    system_message: SystemMessage


class CandidateAgentCandidate(TypedDict, total=False):
    config: Required[AgentConfig]

    type: Required[Literal["agent"]]


Candidate: TypeAlias = Union[CandidateModelCandidate, CandidateAgentCandidate]
