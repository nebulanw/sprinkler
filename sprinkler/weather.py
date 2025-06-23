# THE WEATHER ALWAYS STICKS TOGETHER
# Powered by Open-Meteo
import requests

class CurrentWeather:
    def __init__(self, response: dict):
        self.current_precipitation: float = response['current']['precipitation']
        self.total_precipitation: float = response['daily']['precipitation_sum'][0]

class Weather:
    API_BASE = "https://api.open-meteo.com/v1/forecast"
    def __init__(self, latitude: float, longitude: float, timezone: str):
        self.parameters = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": ["precipitation_sum"],
            "current": ["precipitation"],
            "timezone": timezone
        }

    def query(self):
        forecast = requests.get(self.API_BASE, params=self.parameters).json()
        return CurrentWeather(forecast)

