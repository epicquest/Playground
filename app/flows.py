import asyncio

from prefect import flow, task

from app.main import get_weather_service
from app.models import WeatherData


@task
async def fetch_weather_task(city: str, country_code: str = None) -> WeatherData:
    """Prefect task to fetch weather data"""
    service = get_weather_service()
    return await service.get_weather(city, country_code)


@flow
async def weather_flow(city: str, country_code: str = None) -> WeatherData:
    """Prefect flow for weather data processing"""
    weather_data = await fetch_weather_task(city, country_code)
    return weather_data


# Example of running the flow
async def run_weather_flow():
    result = await weather_flow("London", "UK")
    print(f"Weather flow result: {result}")


if __name__ == "__main__":
    asyncio.run(run_weather_flow())
