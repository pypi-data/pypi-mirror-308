# Shared Types

```python
from llama_stack_client.types import (
    AgentConfig,
    Attachment,
    BatchCompletion,
    CodeInterpreterToolDefinition,
    CompletionMessage,
    FunctionCallToolDefinition,
    GraphMemoryBankDef,
    ImageMedia,
    KeyValueMemoryBankDef,
    KeywordMemoryBankDef,
    MemoryToolDefinition,
    PhotogenToolDefinition,
    SafetyViolation,
    SamplingParams,
    ScoringResult,
    SearchToolDefinition,
    SystemMessage,
    ToolCall,
    ToolParamDefinition,
    ToolResponseMessage,
    UserMessage,
    VectorMemoryBankDef,
    WolframAlphaToolDefinition,
)
```

# Agents

Types:

```python
from llama_stack_client.types import (
    InferenceStep,
    MemoryRetrievalStep,
    RestAPIExecutionConfig,
    ShieldCallStep,
    ToolExecutionStep,
    ToolResponse,
    AgentCreateResponse,
)
```

Methods:

- <code title="post /agents/create">client.agents.<a href="./src/llama_stack_client/resources/agents/agents.py">create</a>(\*\*<a href="src/llama_stack_client/types/agent_create_params.py">params</a>) -> <a href="./src/llama_stack_client/types/agent_create_response.py">AgentCreateResponse</a></code>
- <code title="post /agents/delete">client.agents.<a href="./src/llama_stack_client/resources/agents/agents.py">delete</a>(\*\*<a href="src/llama_stack_client/types/agent_delete_params.py">params</a>) -> None</code>

## Session

Types:

```python
from llama_stack_client.types.agents import Session, SessionCreateResponse
```

Methods:

- <code title="post /agents/session/create">client.agents.session.<a href="./src/llama_stack_client/resources/agents/session.py">create</a>(\*\*<a href="src/llama_stack_client/types/agents/session_create_params.py">params</a>) -> <a href="./src/llama_stack_client/types/agents/session_create_response.py">SessionCreateResponse</a></code>
- <code title="post /agents/session/get">client.agents.session.<a href="./src/llama_stack_client/resources/agents/session.py">retrieve</a>(\*\*<a href="src/llama_stack_client/types/agents/session_retrieve_params.py">params</a>) -> <a href="./src/llama_stack_client/types/agents/session.py">Session</a></code>
- <code title="post /agents/session/delete">client.agents.session.<a href="./src/llama_stack_client/resources/agents/session.py">delete</a>(\*\*<a href="src/llama_stack_client/types/agents/session_delete_params.py">params</a>) -> None</code>

## Steps

Types:

```python
from llama_stack_client.types.agents import StepRetrieveResponse
```

Methods:

- <code title="get /agents/step/get">client.agents.steps.<a href="./src/llama_stack_client/resources/agents/steps.py">retrieve</a>(\*\*<a href="src/llama_stack_client/types/agents/step_retrieve_params.py">params</a>) -> <a href="./src/llama_stack_client/types/agents/step_retrieve_response.py">StepRetrieveResponse</a></code>

## Turn

Types:

```python
from llama_stack_client.types.agents import Turn, TurnCreateResponse
```

Methods:

- <code title="post /agents/turn/create">client.agents.turn.<a href="./src/llama_stack_client/resources/agents/turn.py">create</a>(\*\*<a href="src/llama_stack_client/types/agents/turn_create_params.py">params</a>) -> <a href="./src/llama_stack_client/types/agents/turn_create_response.py">TurnCreateResponse</a></code>
- <code title="get /agents/turn/get">client.agents.turn.<a href="./src/llama_stack_client/resources/agents/turn.py">retrieve</a>(\*\*<a href="src/llama_stack_client/types/agents/turn_retrieve_params.py">params</a>) -> <a href="./src/llama_stack_client/types/agents/turn.py">Turn</a></code>

# BatchInferences

Types:

```python
from llama_stack_client.types import BatchInferenceChatCompletionResponse
```

Methods:

- <code title="post /batch_inference/chat_completion">client.batch_inferences.<a href="./src/llama_stack_client/resources/batch_inferences.py">chat_completion</a>(\*\*<a href="src/llama_stack_client/types/batch_inference_chat_completion_params.py">params</a>) -> <a href="./src/llama_stack_client/types/batch_inference_chat_completion_response.py">BatchInferenceChatCompletionResponse</a></code>
- <code title="post /batch_inference/completion">client.batch_inferences.<a href="./src/llama_stack_client/resources/batch_inferences.py">completion</a>(\*\*<a href="src/llama_stack_client/types/batch_inference_completion_params.py">params</a>) -> <a href="./src/llama_stack_client/types/shared/batch_completion.py">BatchCompletion</a></code>

# Datasets

Types:

```python
from llama_stack_client.types import DatasetRetrieveResponse, DatasetListResponse
```

Methods:

- <code title="get /datasets/get">client.datasets.<a href="./src/llama_stack_client/resources/datasets.py">retrieve</a>(\*\*<a href="src/llama_stack_client/types/dataset_retrieve_params.py">params</a>) -> <a href="./src/llama_stack_client/types/dataset_retrieve_response.py">Optional</a></code>
- <code title="get /datasets/list">client.datasets.<a href="./src/llama_stack_client/resources/datasets.py">list</a>() -> <a href="./src/llama_stack_client/types/dataset_list_response.py">DatasetListResponse</a></code>
- <code title="post /datasets/register">client.datasets.<a href="./src/llama_stack_client/resources/datasets.py">register</a>(\*\*<a href="src/llama_stack_client/types/dataset_register_params.py">params</a>) -> None</code>

# Evaluations

Types:

```python
from llama_stack_client.types import EvaluationEvaluateResponse, EvaluationEvaluateBatchResponse
```

Methods:

- <code title="post /eval/evaluate">client.evaluations.<a href="./src/llama_stack_client/resources/evaluations/evaluations.py">evaluate</a>(\*\*<a href="src/llama_stack_client/types/evaluation_evaluate_params.py">params</a>) -> <a href="./src/llama_stack_client/types/evaluation_evaluate_response.py">EvaluationEvaluateResponse</a></code>
- <code title="post /eval/evaluate_batch">client.evaluations.<a href="./src/llama_stack_client/resources/evaluations/evaluations.py">evaluate_batch</a>(\*\*<a href="src/llama_stack_client/types/evaluation_evaluate_batch_params.py">params</a>) -> <a href="./src/llama_stack_client/types/evaluation_evaluate_batch_response.py">EvaluationEvaluateBatchResponse</a></code>

## Jobs

Types:

```python
from llama_stack_client.types.evaluations import JobRetrieveResponse, JobStatusResponse
```

Methods:

- <code title="get /eval/job/result">client.evaluations.jobs.<a href="./src/llama_stack_client/resources/evaluations/jobs.py">retrieve</a>(\*\*<a href="src/llama_stack_client/types/evaluations/job_retrieve_params.py">params</a>) -> <a href="./src/llama_stack_client/types/evaluations/job_retrieve_response.py">JobRetrieveResponse</a></code>
- <code title="post /eval/job/cancel">client.evaluations.jobs.<a href="./src/llama_stack_client/resources/evaluations/jobs.py">cancel</a>(\*\*<a href="src/llama_stack_client/types/evaluations/job_cancel_params.py">params</a>) -> None</code>
- <code title="get /eval/job/status">client.evaluations.jobs.<a href="./src/llama_stack_client/resources/evaluations/jobs.py">status</a>(\*\*<a href="src/llama_stack_client/types/evaluations/job_status_params.py">params</a>) -> Optional</code>

# Inspect

Types:

```python
from llama_stack_client.types import HealthInfo, ProviderInfo, RouteInfo
```

Methods:

- <code title="get /health">client.inspect.<a href="./src/llama_stack_client/resources/inspect.py">health</a>() -> <a href="./src/llama_stack_client/types/health_info.py">HealthInfo</a></code>

# Inference

Types:

```python
from llama_stack_client.types import (
    CompletionResponse,
    EmbeddingsResponse,
    TokenLogProbs,
    InferenceChatCompletionResponse,
    InferenceCompletionResponse,
)
```

Methods:

- <code title="post /inference/chat_completion">client.inference.<a href="./src/llama_stack_client/resources/inference.py">chat_completion</a>(\*\*<a href="src/llama_stack_client/types/inference_chat_completion_params.py">params</a>) -> <a href="./src/llama_stack_client/types/inference_chat_completion_response.py">InferenceChatCompletionResponse</a></code>
- <code title="post /inference/completion">client.inference.<a href="./src/llama_stack_client/resources/inference.py">completion</a>(\*\*<a href="src/llama_stack_client/types/inference_completion_params.py">params</a>) -> <a href="./src/llama_stack_client/types/inference_completion_response.py">InferenceCompletionResponse</a></code>
- <code title="post /inference/embeddings">client.inference.<a href="./src/llama_stack_client/resources/inference.py">embeddings</a>(\*\*<a href="src/llama_stack_client/types/inference_embeddings_params.py">params</a>) -> <a href="./src/llama_stack_client/types/embeddings_response.py">EmbeddingsResponse</a></code>

# Memory

Types:

```python
from llama_stack_client.types import QueryDocumentsResponse
```

Methods:

- <code title="post /memory/insert">client.memory.<a href="./src/llama_stack_client/resources/memory.py">insert</a>(\*\*<a href="src/llama_stack_client/types/memory_insert_params.py">params</a>) -> None</code>
- <code title="post /memory/query">client.memory.<a href="./src/llama_stack_client/resources/memory.py">query</a>(\*\*<a href="src/llama_stack_client/types/memory_query_params.py">params</a>) -> <a href="./src/llama_stack_client/types/query_documents_response.py">QueryDocumentsResponse</a></code>

# MemoryBanks

Types:

```python
from llama_stack_client.types import MemoryBankRetrieveResponse, MemoryBankListResponse
```

Methods:

- <code title="get /memory_banks/get">client.memory_banks.<a href="./src/llama_stack_client/resources/memory_banks.py">retrieve</a>(\*\*<a href="src/llama_stack_client/types/memory_bank_retrieve_params.py">params</a>) -> <a href="./src/llama_stack_client/types/memory_bank_retrieve_response.py">Optional</a></code>
- <code title="get /memory_banks/list">client.memory_banks.<a href="./src/llama_stack_client/resources/memory_banks.py">list</a>() -> <a href="./src/llama_stack_client/types/memory_bank_list_response.py">MemoryBankListResponse</a></code>
- <code title="post /memory_banks/register">client.memory_banks.<a href="./src/llama_stack_client/resources/memory_banks.py">register</a>(\*\*<a href="src/llama_stack_client/types/memory_bank_register_params.py">params</a>) -> None</code>

# Models

Types:

```python
from llama_stack_client.types import ModelDefWithProvider
```

Methods:

- <code title="get /models/get">client.models.<a href="./src/llama_stack_client/resources/models.py">retrieve</a>(\*\*<a href="src/llama_stack_client/types/model_retrieve_params.py">params</a>) -> <a href="./src/llama_stack_client/types/model_def_with_provider.py">Optional</a></code>
- <code title="get /models/list">client.models.<a href="./src/llama_stack_client/resources/models.py">list</a>() -> <a href="./src/llama_stack_client/types/model_def_with_provider.py">ModelDefWithProvider</a></code>
- <code title="post /models/register">client.models.<a href="./src/llama_stack_client/resources/models.py">register</a>(\*\*<a href="src/llama_stack_client/types/model_register_params.py">params</a>) -> None</code>

# PostTraining

Types:

```python
from llama_stack_client.types import PostTrainingJob
```

Methods:

- <code title="post /post_training/preference_optimize">client.post_training.<a href="./src/llama_stack_client/resources/post_training/post_training.py">preference_optimize</a>(\*\*<a href="src/llama_stack_client/types/post_training_preference_optimize_params.py">params</a>) -> <a href="./src/llama_stack_client/types/post_training_job.py">PostTrainingJob</a></code>
- <code title="post /post_training/supervised_fine_tune">client.post_training.<a href="./src/llama_stack_client/resources/post_training/post_training.py">supervised_fine_tune</a>(\*\*<a href="src/llama_stack_client/types/post_training_supervised_fine_tune_params.py">params</a>) -> <a href="./src/llama_stack_client/types/post_training_job.py">PostTrainingJob</a></code>

## Job

Types:

```python
from llama_stack_client.types.post_training import (
    JobArtifactsResponse,
    JobLogsResponse,
    JobStatusResponse,
)
```

Methods:

- <code title="get /post_training/jobs">client.post_training.job.<a href="./src/llama_stack_client/resources/post_training/job.py">list</a>() -> <a href="./src/llama_stack_client/types/post_training_job.py">PostTrainingJob</a></code>
- <code title="get /post_training/job/artifacts">client.post_training.job.<a href="./src/llama_stack_client/resources/post_training/job.py">artifacts</a>(\*\*<a href="src/llama_stack_client/types/post_training/job_artifacts_params.py">params</a>) -> <a href="./src/llama_stack_client/types/post_training/job_artifacts_response.py">JobArtifactsResponse</a></code>
- <code title="post /post_training/job/cancel">client.post_training.job.<a href="./src/llama_stack_client/resources/post_training/job.py">cancel</a>(\*\*<a href="src/llama_stack_client/types/post_training/job_cancel_params.py">params</a>) -> None</code>
- <code title="get /post_training/job/logs">client.post_training.job.<a href="./src/llama_stack_client/resources/post_training/job.py">logs</a>(\*\*<a href="src/llama_stack_client/types/post_training/job_logs_params.py">params</a>) -> <a href="./src/llama_stack_client/types/post_training/job_logs_response.py">JobLogsResponse</a></code>
- <code title="get /post_training/job/status">client.post_training.job.<a href="./src/llama_stack_client/resources/post_training/job.py">status</a>(\*\*<a href="src/llama_stack_client/types/post_training/job_status_params.py">params</a>) -> <a href="./src/llama_stack_client/types/post_training/job_status_response.py">JobStatusResponse</a></code>

# Providers

Types:

```python
from llama_stack_client.types import ProviderListResponse
```

Methods:

- <code title="get /providers/list">client.providers.<a href="./src/llama_stack_client/resources/providers.py">list</a>() -> <a href="./src/llama_stack_client/types/provider_list_response.py">ProviderListResponse</a></code>

# Routes

Types:

```python
from llama_stack_client.types import RouteListResponse
```

Methods:

- <code title="get /routes/list">client.routes.<a href="./src/llama_stack_client/resources/routes.py">list</a>() -> <a href="./src/llama_stack_client/types/route_list_response.py">RouteListResponse</a></code>

# Safety

Types:

```python
from llama_stack_client.types import RunShieldResponse
```

Methods:

- <code title="post /safety/run_shield">client.safety.<a href="./src/llama_stack_client/resources/safety.py">run_shield</a>(\*\*<a href="src/llama_stack_client/types/safety_run_shield_params.py">params</a>) -> <a href="./src/llama_stack_client/types/run_shield_response.py">RunShieldResponse</a></code>

# Shields

Types:

```python
from llama_stack_client.types import ShieldDefWithProvider
```

Methods:

- <code title="get /shields/get">client.shields.<a href="./src/llama_stack_client/resources/shields.py">retrieve</a>(\*\*<a href="src/llama_stack_client/types/shield_retrieve_params.py">params</a>) -> <a href="./src/llama_stack_client/types/shield_def_with_provider.py">Optional</a></code>
- <code title="get /shields/list">client.shields.<a href="./src/llama_stack_client/resources/shields.py">list</a>() -> <a href="./src/llama_stack_client/types/shield_def_with_provider.py">ShieldDefWithProvider</a></code>
- <code title="post /shields/register">client.shields.<a href="./src/llama_stack_client/resources/shields.py">register</a>(\*\*<a href="src/llama_stack_client/types/shield_register_params.py">params</a>) -> None</code>

# SyntheticDataGeneration

Types:

```python
from llama_stack_client.types import SyntheticDataGenerationResponse
```

Methods:

- <code title="post /synthetic_data_generation/generate">client.synthetic_data_generation.<a href="./src/llama_stack_client/resources/synthetic_data_generation.py">generate</a>(\*\*<a href="src/llama_stack_client/types/synthetic_data_generation_generate_params.py">params</a>) -> <a href="./src/llama_stack_client/types/synthetic_data_generation_response.py">SyntheticDataGenerationResponse</a></code>

# Telemetry

Types:

```python
from llama_stack_client.types import Trace
```

Methods:

- <code title="get /telemetry/get_trace">client.telemetry.<a href="./src/llama_stack_client/resources/telemetry.py">get_trace</a>(\*\*<a href="src/llama_stack_client/types/telemetry_get_trace_params.py">params</a>) -> <a href="./src/llama_stack_client/types/trace.py">Trace</a></code>
- <code title="post /telemetry/log_event">client.telemetry.<a href="./src/llama_stack_client/resources/telemetry.py">log_event</a>(\*\*<a href="src/llama_stack_client/types/telemetry_log_event_params.py">params</a>) -> None</code>

# Datasetio

Types:

```python
from llama_stack_client.types import PaginatedRowsResult
```

Methods:

- <code title="get /datasetio/get_rows_paginated">client.datasetio.<a href="./src/llama_stack_client/resources/datasetio.py">get_rows_paginated</a>(\*\*<a href="src/llama_stack_client/types/datasetio_get_rows_paginated_params.py">params</a>) -> <a href="./src/llama_stack_client/types/paginated_rows_result.py">PaginatedRowsResult</a></code>

# Scoring

Types:

```python
from llama_stack_client.types import ScoringScoreResponse, ScoringScoreBatchResponse
```

Methods:

- <code title="post /scoring/score">client.scoring.<a href="./src/llama_stack_client/resources/scoring.py">score</a>(\*\*<a href="src/llama_stack_client/types/scoring_score_params.py">params</a>) -> <a href="./src/llama_stack_client/types/scoring_score_response.py">ScoringScoreResponse</a></code>
- <code title="post /scoring/score_batch">client.scoring.<a href="./src/llama_stack_client/resources/scoring.py">score_batch</a>(\*\*<a href="src/llama_stack_client/types/scoring_score_batch_params.py">params</a>) -> <a href="./src/llama_stack_client/types/scoring_score_batch_response.py">ScoringScoreBatchResponse</a></code>

# ScoringFunctions

Types:

```python
from llama_stack_client.types import ScoringFnDefWithProvider
```

Methods:

- <code title="get /scoring_functions/get">client.scoring_functions.<a href="./src/llama_stack_client/resources/scoring_functions.py">retrieve</a>(\*\*<a href="src/llama_stack_client/types/scoring_function_retrieve_params.py">params</a>) -> <a href="./src/llama_stack_client/types/scoring_fn_def_with_provider.py">Optional</a></code>
- <code title="get /scoring_functions/list">client.scoring_functions.<a href="./src/llama_stack_client/resources/scoring_functions.py">list</a>() -> <a href="./src/llama_stack_client/types/scoring_fn_def_with_provider.py">ScoringFnDefWithProvider</a></code>
- <code title="post /scoring_functions/register">client.scoring_functions.<a href="./src/llama_stack_client/resources/scoring_functions.py">register</a>(\*\*<a href="src/llama_stack_client/types/scoring_function_register_params.py">params</a>) -> None</code>
