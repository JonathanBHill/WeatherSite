import html

import pandas as pd
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from classes.request import Request as WeatherRequest
import classes.rmdb as db_class
import uvicorn

weather_app = FastAPI()
templates = Jinja2Templates(directory="templates")
weather_app.mount("/static", StaticFiles(directory="static"), name="static")
# from fastapi import FastAPI

# weather_app = FastAPI()


@weather_app.get("/")
async def root(request: Request):
    # dbm = db_class.Database('weather')
    # dbm.wipe_table(db_class.Location)
    # dbm.wipe_table(db_class.Hourly)
    return templates.TemplateResponse("home.html", {"request": request})


@weather_app.get('/cities/{city}/tables')
async def get_city_v2(
        request: Request, city: str,
):
    city = city.capitalize()
    weather_response = WeatherRequest(f'{city} CO')
    hour_response_as_json = weather_response.hour_df.to_json(orient='records')
    astro_response_as_json = weather_response.astro_df.to_json(orient='records')
    daily_response_as_json = weather_response.day_df.to_json(orient='records')
    return templates.TemplateResponse(
        "city-tables.html",
        {
            "request": request,
            "city": city,
            "hjson": html.unescape(hour_response_as_json),
            "ajson": html.unescape(astro_response_as_json),
            "djson": html.unescape(daily_response_as_json),
            "request_api": weather_response
        }
    )
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
def main():
    uvicorn.run(weather_app, host='127.0.0.1', port=8001, log_level='info')


if __name__ == '__main__':
    main()
