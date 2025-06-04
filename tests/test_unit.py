import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from app.services import WeatherService, MockWeatherService
from app.models import WeatherData, WeatherRequest, WeatherResponse
from datetime import datetime
import aiohttp


class TestWeatherService:

    @pytest.mark.asyncio
    async def test_mock_weather_service(self):
        """Test mock weather service"""
        service = MockWeatherService()
        result = await service.get_weather("London")

        assert isinstance(result, WeatherData)
        assert result.temperature == 22.5
        assert result.description == "sunny"
        assert result.humidity == 65

    @pytest.mark.asyncio
    async def test_weather_service_success(self):
        """Test weather service with mocked HTTP response"""
        mock_response_data = {
            "main": {"temp": 15.5, "humidity": 70},
            "weather": [{"description": "cloudy"}]
        }

        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_get.return_value.__aenter__.return_value = mock_response

            service = WeatherService()
            result = await service.get_weather("Paris")

            assert result.temperature == 15.5
            assert result.description == "cloudy"
            assert result.humidity == 70

    @pytest.mark.asyncio
    async def test_weather_service_api_error(self):
        """Test weather service with API error"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 404
            mock_get.return_value.__aenter__.return_value = mock_response

            service = WeatherService()

            with pytest.raises(Exception) as exc_info:
                await service.get_weather("InvalidCity")

            assert "Weather API error: 404" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_weather_service_network_error(self):
        """Test weather service with network error"""
        with patch('aiohttp.ClientSession.get', side_effect=aiohttp.ClientError("Connection failed")):
            service = WeatherService()

            with pytest.raises(Exception) as exc_info:
                await service.get_weather("London")

            assert "Network error" in str(exc_info.value)


class TestModels:

    def test_weather_request_validation(self):
        """Test weather request model validation"""
        # Valid request
        request = WeatherRequest(city="London", country_code="UK")
        assert request.city == "London"
        assert request.country_code == "UK"

        # Invalid request - empty city
        with pytest.raises(ValueError):
            WeatherRequest(city="")

    def test_weather_response_serialization(self):
        """Test weather response model serialization"""
        response = WeatherResponse(
            city="London",
            temperature=20.5,
            description="sunny",
            humidity=60,
            timestamp=datetime(2024, 1, 1, 12, 0, 0)
        )

        data = response.model_dump()
        assert data["city"] == "London"
        assert data["temperature"] == 20.5
        assert isinstance(data["timestamp"], datetime)