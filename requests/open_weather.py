import aiohttp
import os

class OpenWeatherMapApi:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    async def get_current_weather(self, city: str):
        url = f"{self.base_url}?q={city}&appid={self.api_key}&units=metric"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return None  # Или обработать ошибку