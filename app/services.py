import asyncio
import logging
from typing import Optional

import aiohttp

from app.models import WeatherData

logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self, api_key: str = "dummy_key"):
        self.api_key = api_key
        logging.debug(f"Using key: {api_key}")
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
                    else:
                        logger.error(f"API error: {response.status}")
                        raise Exception(f"Weather API error: {response.status}")
            except aiohttp.ClientError as e:
                logger.error(f"Network error: {e}")
                raise Exception(f"Network error: {str(e)}")


class MockWeatherService(WeatherService):
    """Mock service for testing"""

    async def get_weather(
        self, city: str, country_code: Optional[str] = None
    ) -> WeatherData:
        await asyncio.sleep(0.1)  # Simulate API delay
        return WeatherData(temperature=22.5, description="sunny", humidity=65)
