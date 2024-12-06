# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import datetime
from typing import Union
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["GreeksFlowRetrieveParams"]


class GreeksFlowRetrieveParams(TypedDict, total=False):
    date: Annotated[Union[str, datetime.date], PropertyInfo(format="iso8601")]
    """Date to filter the Greek flow data."""

    max_delta: Annotated[float, PropertyInfo(alias="maxDelta")]
    """Maximum delta value."""

    min_delta: Annotated[float, PropertyInfo(alias="minDelta")]
    """Minimum delta value."""

    symbol: str
    """Stock symbol to filter the Greek flow data."""
