# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["EvaluationEvaluateResponse", "Metric"]


class Metric(BaseModel):
    id: str

    deployment_status: str = FieldInfo(alias="deploymentStatus")

    description: str

    name: str


class EvaluationEvaluateResponse(BaseModel):
    metric: Metric

    scores: List[float]
