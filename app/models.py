from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class WeatherRequest(BaseModel):
    city: str = Field(..., min_length=1, max_length=100)
    country_code: Optional[str] = Field(None, max_length=2)


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    timestamp: datetime

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class WeatherData(BaseModel):
    temperature: float
    description: str
    humidity: int
