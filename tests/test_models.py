from requests.models import City

def test_city_model():
    """Проверяет атрибуты модели City."""
    city = City(city="Test City", views=10)

    assert city.id is None
    assert city.city == "Test City"
    assert city.views == 10
