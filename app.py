from fastapi import FastAPI
from weather import app as weather_app
from planner import app as planner_app
import uvicorn

app = FastAPI()

# Mount the sub-applications at different prefixes
app.mount("/weather", weather_app)
app.mount("/plan", planner_app)

@app.get("/")
def root():
    return {
        "message": "Travel Agent API",
        "endpoints": {
            "weather": "weather/forecast",
            "planner": "plan/generate"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
