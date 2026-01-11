from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    api_key=os.environ["HF_TOKEN"],
)
app = FastAPI()

class TravelRequest(BaseModel):
    destination: str
    start: str
    end: str
    commute: List[str]
    focus: List[str]
    specifics: str

def call_llm(prompt: str):
    try:
        completion = client.chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=700,
            temperature=0.7
        )
        
        if completion is None or "choices" not in completion or len(completion.choices) == 0:
            return "Error: No response from the language model.", 0
        
        return completion.choices[0].message["content"], 1
        
    except Exception as e:
        return f"Error: {str(e)}", 0
    
@app.post("/generate-plan")
def generate_plan(req: TravelRequest):

    prompt = f"""
You are a professional travel planner.

Create a detailed travel itinerary.

Destination: {req.destination};
Start Date: {req.start};
End Date: {req.end};
Preferred commute: {", ".join(req.commute)};
Key interests: {", ".join(req.focus)};
Specific requests: {req.specifics};

Rules:
- Provide a day-by-day plan
- Include food, attractions, and tips
- Keep it practical and realistic
"""

    plan, status = call_llm(prompt)

    return {"plan": plan, "status": status}