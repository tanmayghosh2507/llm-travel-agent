from fastapi import FastAPI, responses
import requests

from constants import GET_GEOCODING, GET_WEATHER
from utils import get_past_recent_date
import openmeteo_requests
import requests_cache
from retry_requests import retry
import numpy as np

app = FastAPI()
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

@app.get("/forecast")
def get_weather_forecast(city: str, start_date: str, end_date: str) -> str:
    print(f"Fetching Geocoding for {city} from {start_date} to {end_date}")
    try:
        lat, lon = get_lat_lon(city)
    except Exception as e:
        return f"Error retrieving location: {str(e)}"
    
    print(f"Fetching weather for {city} (lat: {lat}, lon: {lon}) from {start_date} to {end_date}")
    
    try:
        url = GET_WEATHER
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": get_past_recent_date(start_date),
            "end_date": get_past_recent_date(end_date),
            "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "daylight_duration", "sunrise", "sunset"],
        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_mean = daily.Variables(2).ValuesAsNumpy()
        daily_daylight_duration = daily.Variables(3).ValuesAsNumpy()
        weather_response = f"The weather in {city} from {start_date} to {end_date} is expected to be ranging from {np.min(daily_temperature_2m_min):.1f}C to {np.max(daily_temperature_2m_max):.1f}C with mean: {np.mean(daily_temperature_2m_mean):.1f}C and approximately {(np.mean(daily_daylight_duration)/3600):.1f} hours of daylight each day."
        return weather_response

    except requests.exceptions.Timeout:
        raise Exception("Request timed out. Please try again in a moment.")
    except requests.exceptions.ConnectionError:
        raise Exception("Connection error.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    

def get_lat_lon(city: str):
    try:
        response = requests.get(GET_GEOCODING.format(city=city), timeout=150)
        result = response.json()

        if isinstance(result, dict) and "results" in result and len(result["results"]) > 0:
            lat = result["results"][0]["latitude"]
            lon = result["results"][0]["longitude"]
            print(f"Got coordinates: lat={lat}, lon={lon}")
            return lat, lon
        else:
            raise Exception(f"Could not retrieve latitude and longitude. Response: {result}")
    except Exception as e:
        raise Exception(f"Error in get_lat_lon: {str(e)}")