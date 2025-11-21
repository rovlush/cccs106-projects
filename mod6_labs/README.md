🌤️ Weather App (Flet v0.28.3)

A simple weather application built using Flet, OpenWeatherMap API, and Python.
The app allows users to enter a city name and view real-time weather information such as temperature, humidity, pressure, wind speed, and cloudiness.

🔧 Requirements

Install the required dependencies:

pip install -r requirements.txt


Your requirements.txt should include:

flet==0.28.3
httpx>=0.25.0
python-dotenv>=1.0.0

🔑 Environment Variables

Create a .env file in your project folder:

OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5/weather

▶️ How to Run the App
1. Activate your virtual environment

Windows:

venv\Scripts\activate

2. Run the application
python main.py

🌍 Features

Search weather by city name

Clean and modern UI (Flet 0.28.3)

Displays:

Temperature

Weather description

Humidity

Wind speed

Pressure

Cloudiness

Error handling for invalid city names

Uses OpenWeatherMap API