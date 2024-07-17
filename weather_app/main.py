from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from requests.models import City
from requests.open_weather import OpenWeatherMapApi
from requests.database import SessionLocal, get_db

app = FastAPI()
templates = Jinja2Templates(directory="openWeatherMap/templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/forecast")
async def forecast(request: Request, city: str = Form(...), db: SessionLocal = Depends(get_db)):
    city = city.strip().lower()
    if not city:
        return templates.TemplateResponse("index.html", {"request": request, "error": "City cannot be empty."})

    db_city = db.query(City).filter(City.city == city).first()
    if db_city is None:
        db_city = City(city=city, views=1)
        db.add(db_city)
    else:
        db_city.views += 1
    db.commit()

    open_weather_api = OpenWeatherMapApi("5a2334c8331d117fedecc011997d9aee")
    weather = await open_weather_api.get_current_weather(city)
    return templates.TemplateResponse("forecast.html", {"request": request, "city": db_city, "weather": weather})


@app.get("/history")
async def history(request: Request, db: SessionLocal = Depends(get_db)):
    cities = db.query(City).order_by(City.views.desc()).limit(5).all()
    return templates.TemplateResponse("history.html", {"request": request, "cities": cities})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
