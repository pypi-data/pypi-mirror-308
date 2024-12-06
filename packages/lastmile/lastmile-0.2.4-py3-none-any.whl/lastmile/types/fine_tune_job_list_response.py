# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "FineTuneJobListResponse",
    "Job",
    "JobID",
    "JobConfig",
    "JobConfigBaselineModelID",
    "JobConfigTestDatasetID",
    "JobConfigTrainDatasetID",
    "JobResult",
    "JobResultProgress",
    "JobResultProgressJobID",
    "JobResultTrainedModelFile",
    "JobResultTrainedModelFileID",
    "JobResultTrainedModelFileModelID",
]


class JobID(BaseModel):
    value: str


class JobConfigBaselineModelID(BaseModel):
    value: str


class JobConfigTestDatasetID(BaseModel):
    value: str


class JobConfigTrainDatasetID(BaseModel):
    value: str


class JobConfig(BaseModel):
    baseline_model_id: JobConfigBaselineModelID = FieldInfo(alias="baselineModelId")

    selected_columns: List[str] = FieldInfo(alias="selectedColumns")
    """
    Set of columns to be used in fine-tuning. Supported columns: input, output,
    ground_truth For example, a task similar to summarization might need output and
    ground_truth.
    """

    test_dataset_id: JobConfigTestDatasetID = FieldInfo(alias="testDatasetId")

    train_dataset_id: JobConfigTrainDatasetID = FieldInfo(alias="trainDatasetId")

    description: Optional[str] = None
    """Optional description for the job."""

    name: Optional[str] = None
    """Optional name for the job."""


class JobResultProgressJobID(BaseModel):
    value: str


class JobResultProgress(BaseModel):
    accuracy: float

    epoch: int

    job_id: JobResultProgressJobID = FieldInfo(alias="jobId")

    loss: float

    progress: float

    timestamp: datetime


class JobResultTrainedModelFileID(BaseModel):
    value: str


class JobResultTrainedModelFileModelID(BaseModel):
    value: str


class JobResultTrainedModelFile(BaseModel):
    id: JobResultTrainedModelFileID

    content_md5_hash: str = FieldInfo(alias="contentMd5Hash")

    created_at: datetime = FieldInfo(alias="createdAt")

    file_size_bytes: int = FieldInfo(alias="fileSizeBytes")

    model_id: JobResultTrainedModelFileModelID = FieldInfo(alias="modelId")

    updated_at: datetime = FieldInfo(alias="updatedAt")


class JobResult(BaseModel):
    progress: List[JobResultProgress]
    """Sequential snapshots of training metrics."""

    result_url: Optional[str] = FieldInfo(alias="resultUrl", default=None)
    """Url to view the full results and progress (e.g. external W&B url)"""

    trained_model_file: Optional[JobResultTrainedModelFile] = FieldInfo(alias="trainedModelFile", default=None)
    """Actual file asset corresponding to a model"""


class Job(BaseModel):
    id: JobID

    config: JobConfig
    """
    Set of columns to be used in fine-tuning. Supported columns: input, output,
    ground_truth For example, a task similar to summarization might need output and
    ground_truth.
    """

    created_at: datetime = FieldInfo(alias="createdAt")

    result: JobResult
    """Sequential snapshots of training metrics."""

    status: str

    updated_at: datetime = FieldInfo(alias="updatedAt")

    description: Optional[str] = None

    name: Optional[str] = None
    """Name corresponding to the fine tuned model derived from this job"""


class FineTuneJobListResponse(BaseModel):
    jobs: List[Job]

    total_count: int = FieldInfo(alias="totalCount")
    """
    Total count of fine tune jobs which can be listed with applicable filters,
    regardless of page size
    """
