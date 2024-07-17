import pytest
import asyncio
from unittest.mock import AsyncMock
from requests.open_weather import OpenWeatherMapApi  # Импортируйте ваш класс

# Фикстура для создания экземпляра класса OpenWeatherMapApi
@pytest.fixture
def api_client():
    api_key = "test_api_key"  #  Можете использовать переменную окружения
    return OpenWeatherMapApi(api_key)

# Моки для aiohttp
@pytest.fixture
def mock_response_success(monkeypatch):
    async def mock_get(*args, **kwargs):
        return MockAsyncResponse(200, {"main": {"temp": 25.5}})
    monkeypatch.setattr("aiohttp.ClientSession.get", mock_get)

@pytest.fixture
def mock_response_failure(monkeypatch):
    async def mock_get(*args, **kwargs):
        return MockAsyncResponse(404, {"message": "City not found"})
    monkeypatch.setattr("aiohttp.ClientSession.get", mock_get)

# Класс-заглушка для имитации ответа aiohttp
class MockAsyncResponse:
    def __init__(self, status, json_data):
        self.status = status
        self._json_data = json_data

    async def json(self):
        return self._json_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

# Тесты
@pytest.mark.asyncio  # Отмечаем тест как асинхронный
async def test_get_current_weather_success(api_client, mock_response_success):
    weather_data = await api_client.get_current_weather("Moscow")
    assert weather_data["main"]["temp"] == 25.5

@pytest.mark.asyncio
async def test_get_current_weather_failure(api_client, mock_response_failure):
    weather_data = await api_client.get_current_weather("InvalidCity")
    assert weather_data is None
