# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "LabelDatasetJobGetStatusResponse",
    "PseudoLabelJobResult",
    "PseudoLabelJobResultChatCompletionConfig",
    "PseudoLabelJobResultChatCompletionConfigMessage",
    "PseudoLabelJobResultPromptTemplate",
]


class PseudoLabelJobResultChatCompletionConfigMessage(BaseModel):
    content: str
    """The content of the message."""

    role: str
    """Role can be 'system', 'user', or 'assistant'."""


class PseudoLabelJobResultChatCompletionConfig(BaseModel):
    max_tokens: int = FieldInfo(alias="maxTokens")
    """The maximum number of tokens to generate."""

    messages: List[PseudoLabelJobResultChatCompletionConfigMessage]
    """The list of messages in the conversation so far."""

    model: str
    """The ID of the model to use for the completion."""

    temperature: float
    """The temperature to use for the completion."""

    top_p: float = FieldInfo(alias="topP")
    """The top_p value to use for the completion."""

    vendor: str


class PseudoLabelJobResultPromptTemplate(BaseModel):
    id: str

    template: str
    """The template string that defines the prompt"""


class PseudoLabelJobResult(BaseModel):
    base_evaluation_metric: str = FieldInfo(alias="baseEvaluationMetric")
    """
    TODO: @Ankush flesh out default prompt templates or "Base Metric" representation
    of prompt lmai.proto.model_fine_tuning.v1.templates.
    """

    chat_completion_config: PseudoLabelJobResultChatCompletionConfig = FieldInfo(alias="chatCompletionConfig")
    """The list of messages in the conversation so far."""

    dataset_id: str = FieldInfo(alias="datasetId")
    """ID of the main dataset to be pseudo-labeled"""

    few_shot_dataset_id: str = FieldInfo(alias="fewShotDatasetId")
    """ID of the dataset containing few-shot examples. Optional."""

    prompt_template: PseudoLabelJobResultPromptTemplate = FieldInfo(alias="promptTemplate")

    selected_columns: List[str] = FieldInfo(alias="selectedColumns")
    """
    Subset of columns to be used in pseudo-labeling. Expected columns: input,
    output, ground_truth For example, a summarization task might not need an input
    column. TODO: Should this be repeated EvaluationMetricParameter enum?
    """

    skip_active_labeling: bool = FieldInfo(alias="skipActiveLabeling")
    """
    If true, skip active labeling, which involves an intermediate Dataset created
    for human labeling.
    """

    active_labeled_dataset_id: Optional[str] = FieldInfo(alias="activeLabeledDatasetId", default=None)
    """ID of the actively labeled dataset.

    Optional. If null, this job is for active learning.
    """

    description: Optional[str] = None
    """Optional description for the job."""

    name: Optional[str] = None
    """Optional name for the job."""


class LabelDatasetJobGetStatusResponse(BaseModel):
    pseudo_label_job_result: PseudoLabelJobResult = FieldInfo(alias="pseudoLabelJobResult")
    """
    Subset of columns to be used in pseudo-labeling. Expected columns: input,
    output, ground_truth For example, a summarization task might not need an input
    column. TODO: Should this be repeated EvaluationMetricParameter enum?
    """

    status: str
