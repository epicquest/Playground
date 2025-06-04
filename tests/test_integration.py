import asyncio

import pytest
import os
from fastapi.testclient import TestClient
from app.main import app

# Set testing environment
os.environ["TESTING"] = "1"

client = TestClient(app)


class TestWeatherAPI:

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_post_weather_endpoint(self):
        """Test POST weather endpoint"""
        payload = {
            "city": "London",
            "country_code": "UK"
        }

        response = client.post("/weather", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["city"] == "London"
        assert data["temperature"] == 22.5
        assert data["description"] == "sunny"
        assert data["humidity"] == 65
        assert "timestamp" in data

    def test_get_weather_by_path(self):
        """Test GET weather endpoint with path parameter"""
        response = client.get("/weather/Paris?country_code=FR")
        assert response.status_code == 200

        data = response.json()
        assert data["city"] == "Paris"
        assert data["temperature"] == 22.5

    def test_post_weather_invalid_data(self):
        """Test POST weather endpoint with invalid data"""
        payload = {
            "city": "",  # Empty city should fail validation
            "country_code": "UK"
        }

        response = client.post("/weather", json=payload)
        assert response.status_code == 422  # Validation error

    def test_get_weather_path_only(self):
        """Test GET weather endpoint with city only"""
        response = client.get("/weather/Tokyo")
        assert response.status_code == 200

        data = response.json()
        assert data["city"] == "Tokyo"


class TestAsyncIntegration:

    @pytest.mark.asyncio
    async def test_async_weather_flow(self):
        """Test async operations work correctly"""
        from app.services import MockWeatherService

        service = MockWeatherService()

        # Test multiple concurrent requests
        tasks = [
            service.get_weather("London"),
            service.get_weather("Paris"),
            service.get_weather("Tokyo")
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 3
        for result in results:
            assert result.temperature == 22.5
            assert result.description == "sunny"