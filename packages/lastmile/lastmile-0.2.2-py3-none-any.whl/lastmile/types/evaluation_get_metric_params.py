# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EvaluationGetMetricParams", "Metric"]


class EvaluationGetMetricParams(TypedDict, total=False):
    metric: Required[Metric]


class Metric(TypedDict, total=False):
    id: Required[str]

    deployment_status: Required[Annotated[str, PropertyInfo(alias="deploymentStatus")]]

    description: Required[str]

    name: Required[str]
