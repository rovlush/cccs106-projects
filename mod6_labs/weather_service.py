# weather_service.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()  # loads OPENWEATHER_API_KEY from .env

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_weather(city):
    """
    Fetch weather information from OpenWeatherMap API.
    Returns a normalized dictionary matching what main.py expects.
    """

    if not API_KEY:
        raise Exception("API Key not found. Please set OPENWEATHER_API_KEY in your .env file.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(BASE_URL, params=params)

        if response.status_code == 404:
            raise Exception(f"City '{city}' not found.")

        if response.status_code == 401:
            raise Exception("Invalid API key. Please check your OPENWEATHER_API_KEY.")

        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")

        data = response.json()

    # Normalize and return the data for the UI
    return {
        "city": data.get("name"),
        "country": data.get("sys", {}).get("country"),

        "temperature": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "temp_max": data.get("main", {}).get("temp_max"),
        "temp_min": data.get("main", {}).get("temp_min"),

        "humidity": data.get("main", {}).get("humidity"),
        "pressure": data.get("main", {}).get("pressure"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "cloudiness": data.get("clouds", {}).get("all"),

        "description": data.get("weather", [{}])[0].get("description", "").title(),
    }