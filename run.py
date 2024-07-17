import uvicorn
import sys


sys.path.append('/home/ara/PycharmProjects/weather_new')

if __name__ == "__main__":
    uvicorn.run("weather_app.main:app", host="127.0.0.1", port=8000, reload=True)
