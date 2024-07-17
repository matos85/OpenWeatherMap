import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from weather_app.main import app, get_db
from requests.models import City

# Настройка тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    City.__table__.create(bind=engine) # Создаем таблицу для каждой тестовой функции
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        City.__table__.drop(bind=engine)  # Удаляем таблицу после теста


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

# Тесты
@pytest.mark.asyncio
async def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Enter a city" in response.text  # Проверяем наличие текста на странице

@pytest.mark.asyncio
async def test_forecast_new_city(client, db, monkeypatch):
    mock_weather_response = {"main": {"temp": 25.5}}

    async def mock_get_current_weather(self, city: str):
        return mock_weather_response

    monkeypatch.setattr("requests.open_weather.OpenWeatherMapApi.get_current_weather", mock_get_current_weather)

    response = client.post("/forecast", data={"city": "Moscow"})
    assert response.status_code == 200
    assert "Moscow" in response.text
    assert "25.5" in response.text

    # Проверяем, что город добавлен в базу данных
    city_in_db = db.query(City).filter(City.city == "moscow").first()
    assert city_in_db is not None
    assert city_in_db.views == 1

@pytest.mark.asyncio
async def test_forecast_existing_city(client, db, monkeypatch):
    mock_weather_response = {"main": {"temp": 28.0}}
    monkeypatch.setattr("requests.open_weather.OpenWeatherMapApi.get_current_weather",
                        lambda self, city: mock_weather_response)

    # Добавляем город в базу данных заранее
    db.add(City(city="London", views=2))
    db.commit()

    response = client.post("/forecast", data={"city": "London"})
    assert response.status_code == 200

    # Проверяем, что количество просмотров увеличилось
    city_in_db = db.query(City).filter(City.city == "london").first()
    assert city_in_db.views == 3

@pytest.mark.asyncio
async def test_history(client, db):
    db.add(City(city="Paris", views=5))
    db.add(City(city="Berlin", views=3))
    db.commit()

    response = client.get("/history")
    assert response.status_code == 200

    # Проверяем порядок городов в истории
    assert "Paris" in response.text
    assert "Berlin" in response.text
