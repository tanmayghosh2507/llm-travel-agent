GET_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
GET_WEATHER = "https://archive-api.open-meteo.com/v1/archive"

# internal
API_PORT = "8000"
API_HOST = "localhost"
GENERATE_PLAN_ENDPOINT = f"http://{API_HOST}:{API_PORT}/plan/generate"
WEATHER_FORECAST_ENDPOINT = "http://localhost:8000/weather/forecast?city={city}&start_date={start_date}&end_date={end_date}"