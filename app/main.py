import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException

from app.models import WeatherRequest, WeatherResponse
from app.services import MockWeatherService, WeatherService

load_dotenv()

app = FastAPI(title="Weather Service API", version="1.0.0")


# Dependency injection for service
def get_weather_service() -> WeatherService:
    if os.getenv("TESTING"):
        return MockWeatherService()

    return WeatherService(api_key=os.getenv("WEATHER_API_KEY", "dummy_key"))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}


@app.post("/weather", response_model=WeatherResponse)
async def get_weather(
    request: WeatherRequest, service: WeatherService = Depends(get_weather_service)
):
    """Get weather data for a city"""
    try:
        weather_data = await service.get_weather(request.city, request.country_code)
        return WeatherResponse(
            city=request.city,
            temperature=weather_data.temperature,
            description=weather_data.description,
            humidity=weather_data.humidity,
            timestamp=datetime.now(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/weather/{city}")
async def get_weather_by_path(
    city: str,
    country_code: str = None,
    service: WeatherService = Depends(get_weather_service),
):
    """Get weather data using path parameter"""
    try:
        weather_data = await service.get_weather(city, country_code)
        return WeatherResponse(
            city=city,
            temperature=weather_data.temperature,
            description=weather_data.description,
            humidity=weather_data.humidity,
            timestamp=datetime.now(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
