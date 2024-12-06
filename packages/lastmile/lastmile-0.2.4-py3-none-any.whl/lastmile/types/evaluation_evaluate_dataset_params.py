# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EvaluationEvaluateDatasetParams", "DatasetID", "Metric"]


class EvaluationEvaluateDatasetParams(TypedDict, total=False):
    dataset_id: Required[Annotated[DatasetID, PropertyInfo(alias="datasetId")]]

    metric: Required[Metric]


class DatasetID(TypedDict, total=False):
    value: Required[str]


class Metric(TypedDict, total=False):
    id: str

    deployment_status: Annotated[str, PropertyInfo(alias="deploymentStatus")]

    description: str

    name: str
