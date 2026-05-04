import requests
import random

API_KEY = "YOUR_OPENWEATHER_API_KEY"

def get_live_environment():
    return {
        "humidity": random.randint(60, 85),
        "sunshine": random.randint(6, 10)
    }

def get_real_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"]
    }