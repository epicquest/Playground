"""
Models module.

Data models for REST.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_serializer


class WeatherRequest(BaseModel):
    """Request model containing city and optional 2-letter country code."""
    city: str = Field(..., min_length=1, max_length=100)
    country_code: Optional[str] = Field(None, max_length=2)


class WeatherResponse(BaseModel):
    """Response model containing data about weather."""
    city: str
    temperature: float
    description: str
    humidity: int
    timestamp: datetime

    @field_serializer('timestamp')
    def serialize_timestamp(self, value: datetime) -> str:
        """date serialization"""
        return value.isoformat()

class WeatherData(BaseModel):
    """Data model containing data about weather."""
    temperature: float
    description: str
    humidity: int
