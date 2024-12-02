import requests

from typing import Union
from fastapi import FastAPI, Path
# Позволяет отправить ответ в виде HTML
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from starlette.responses import FileResponse
from starlette.routing import request_response


# Создаем объект приложения
app = FastAPI()
response = requests.get("https://openexchangerates.org/api/")
weatherstack_api_key = "0311eb0407e84e09b6fc642983136245"


cities = {
    "New York": "40.7128  -74.0060",
    "London": "51.5074  -0.1278",
    "Paris": "48.8566  2.3522",
    "Tokyo": "35.6762  139.6503",
    "Sydney": "-33.8651  151.2093",
    "Rio de Janeiro": "-22.9068  -43.1729",
    "Dubai": "25.2048  55.2708",
    "Mumbai": "19.0760  72.8777",
    "Hong Kong": "22.3193  114.1694",
    "Singapore": "1.3521  103.8198",
    "Toronto": "43.6532  -79.3832",
    "Berlin": "52.5200  13.4050",
    "Moscow": "55.7558  37.6173",
    "Beijing": "39.9042  116.4074",
    "Bangkok": "13.7563  100.5018",
    "Cairo": "30.0444  31.2357",
    "Istanbul": "41.0082  28.9784",
    "São Paulo": "-23.5505  -46.6333",
    "Mexico City": "19.4326  -99.1332",
    "New Delhi": "28.6139  77.2090"
}


class Currency(BaseModel):
    cur: str
    value: float



# Запрос в корень
@app.get("/")
async def read_root():
    html_content = "<h2>Hello METANIT.COM!</h2>"
    return HTMLResponse(content=html_content)


# Запрос в корень
@app.get("/about", response_class=FileResponse)
async def read_root():
    return "index.html"


# Запрос по items
@app.get("/currencies/{currency_id}")
async def current_course(currency:str = Path(min_length=2, max_length=4)):
    return {"currency": currency}


#
@app.post("/weather", response_class=HTMLResponse)
async def weather(request: Request, location: str = Form(...), units: str = "m"):
    # Create the API url with the location and units parameters
    url = f"http://api.weatherstack.com/forecast?access_key={weatherstack_api_key}&query={location}&units={units}"
    # Send a GET request to the API url
    response = requests.get(url)

    if response.status_code == 200:
        # If the response status code is 200, then retrieve the JSON data from the response
        data = response.json()

        # Extract the required weather data from the JSON object and store it in a dictionary
        weather = {
            "location": data["location"]["name"],
            "temperature": data["current"]["temperature"],
            "humidity": data["current"]["humidity"],
            "wind_speed": data["current"]["wind_speed"],
            "description": data["current"]["weather_descriptions"][0],
            "icon": data["current"]["weather_icons"][0],
            "forecast": data.get("forecast", {}).get("forecastday", [{}])[0].get("day", {}).get("condition", {}).get("text", ""),
            "forecast_icon": data.get("forecast", {}).get("forecastday", [{}])[0].get("day", {}).get("condition", {}).get("icon", {}).get("url", "")

        }

        # Render the weather.html template with the weather data dictionary as context
        return templates.TemplateResponse("weather.html", {"request": request, "weather": weather})

    else:
        # If the response status code is not 200, then render the error.html template with an error message
        return templates.TemplateResponse("error.html",
                                          {"request": request, "error": "Could not retrieve weather data."})