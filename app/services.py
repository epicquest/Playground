# pylint: disable=too-few-public-methods
"""
Services module.

This script contains async communication with external api and mocked version of service.
"""

import asyncio
import logging
from typing import Optional

import aiohttp
from fastapi import HTTPException

from app.models import WeatherData

logger = logging.getLogger(__name__)

"""
Services class.
"""


class WeatherService:
    """
    Service for fetching weather data from OpenWeatherMap API.

    Attributes:
        api_key (str): API key for authentication.
        base_url (str): Base URL for the weather API endpoint.
    """

    def __init__(self, api_key: str = "dummy_key"):
        self.api_key = api_key
        logging.debug("Using key: %s", api_key)
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    async def get_weather(
        self, city: str, country_code: Optional[str] = None
    ) -> WeatherData:
        """Fetch weather data from external API"""
        location = f"{city},{country_code}" if country_code else city

        params = {"q": location, "appid": self.api_key, "units": "metric"}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return WeatherData(
                            temperature=data["main"]["temp"],
                            description=data["weather"][0]["description"],
                            humidity=data["main"]["humidity"],
                        )
                    logger.error("API error: %s", response.status)
                    raise HTTPException(
                        status_code=500, detail=f"Weather API error: {response.status}"
                    )
            except aiohttp.ClientError as e:
                logger.error("Network error:  %s", e)
                raise HTTPException(
                    status_code=500, detail=f"Network error: {str(e)}"
                ) from e


class MockWeatherService(WeatherService):
    """Mock service for testing"""

    async def get_weather(
        self, city: str, country_code: Optional[str] = None
    ) -> WeatherData:
        await asyncio.sleep(0.1)  # Simulate API delay
        return WeatherData(temperature=22.5, description="sunny", humidity=65)
