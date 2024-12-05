# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "FineTuneJobCreateParams",
    "FineTuneJobConfig",
    "FineTuneJobConfigBaselineModelID",
    "FineTuneJobConfigTestDatasetID",
    "FineTuneJobConfigTrainDatasetID",
]


class FineTuneJobCreateParams(TypedDict, total=False):
    fine_tune_job_config: Required[Annotated[FineTuneJobConfig, PropertyInfo(alias="fineTuneJobConfig")]]
    """
    Set of columns to be used in fine-tuning. Supported columns: input, output,
    ground_truth For example, a task similar to summarization might need output and
    ground_truth.
    """


class FineTuneJobConfigBaselineModelID(TypedDict, total=False):
    value: Required[str]


class FineTuneJobConfigTestDatasetID(TypedDict, total=False):
    value: Required[str]


class FineTuneJobConfigTrainDatasetID(TypedDict, total=False):
    value: Required[str]


class FineTuneJobConfig(TypedDict, total=False):
    baseline_model_id: Required[Annotated[FineTuneJobConfigBaselineModelID, PropertyInfo(alias="baselineModelId")]]

    selected_columns: Required[Annotated[List[str], PropertyInfo(alias="selectedColumns")]]
    """
    Set of columns to be used in fine-tuning. Supported columns: input, output,
    ground_truth For example, a task similar to summarization might need output and
    ground_truth.
    """

    test_dataset_id: Required[Annotated[FineTuneJobConfigTestDatasetID, PropertyInfo(alias="testDatasetId")]]

    train_dataset_id: Required[Annotated[FineTuneJobConfigTrainDatasetID, PropertyInfo(alias="trainDatasetId")]]

    description: str
    """Optional description for the job."""

    name: str
    """Optional name for the job."""
