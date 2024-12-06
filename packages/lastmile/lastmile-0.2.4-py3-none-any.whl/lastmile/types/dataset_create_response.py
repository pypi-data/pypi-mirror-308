# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "DatasetCreateResponse",
    "Dataset",
    "DatasetID",
    "DatasetColumn",
    "DatasetColumnID",
    "DatasetOwnerUserID",
    "DatasetLabelState",
]


class DatasetID(BaseModel):
    value: str


class DatasetColumnID(BaseModel):
    value: str


class DatasetColumn(BaseModel):
    id: DatasetColumnID

    created_at: datetime = FieldInfo(alias="createdAt")

    index: int
    """Index of the column within the dataset file."""

    literal_name: str = FieldInfo(alias="literalName")
    """The literal name for the column."""

    updated_at: datetime = FieldInfo(alias="updatedAt")

    dtype: Optional[str] = None


class DatasetOwnerUserID(BaseModel):
    value: str


class DatasetLabelState(BaseModel):
    labeling_status: str = FieldInfo(alias="labelingStatus")
    """The status of the latest general pseudo-labeling job for the dataset"""

    prompt_template: str = FieldInfo(alias="promptTemplate")
    """aka user general instructions"""

    error: Optional[str] = None
    """if the labeling status is error, this field may contain an error message"""


class Dataset(BaseModel):
    id: DatasetID

    columns: List[DatasetColumn]
    """The columns present in the latest DatasetFile for this dataset"""

    created_at: datetime = FieldInfo(alias="createdAt")

    initialization_status: str = FieldInfo(alias="initializationStatus")

    num_cols: int = FieldInfo(alias="numCols")

    num_rows: int = FieldInfo(alias="numRows")

    owner_user_id: DatasetOwnerUserID = FieldInfo(alias="ownerUserId")

    updated_at: datetime = FieldInfo(alias="updatedAt")

    description: Optional[str] = None
    """Human-readable description of the dataset, if one exists."""

    initialization_error: Optional[str] = FieldInfo(alias="initializationError", default=None)

    label_state: Optional[DatasetLabelState] = FieldInfo(alias="labelState", default=None)

    name: Optional[str] = None
    """Human-readable name for the dataset, if one exists."""


class DatasetCreateResponse(BaseModel):
    dataset: Dataset
    """The columns present in the latest DatasetFile for this dataset"""
