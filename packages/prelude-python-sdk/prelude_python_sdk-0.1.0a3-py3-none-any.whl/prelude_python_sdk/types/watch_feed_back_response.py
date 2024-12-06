# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["WatchFeedBackResponse"]


class WatchFeedBackResponse(BaseModel):
    id: Optional[str] = None
    """A unique identifier for your feedback request."""
