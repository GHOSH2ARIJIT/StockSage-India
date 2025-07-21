from fastapi import FastAPI
from pydantic import BaseModel
from mongodb import db  # your mongo client

fastapi_app = FastAPI()


class Prediction(BaseModel):
    company: str
    prediction: str
    confidence: float

@fastapi_app.post("/fastapi/save/")
async def save_data(data: Prediction):
    # Convert Pydantic object to dict
    result = await db.predictions.insert_one(data.dict())
    return {"inserted_id": str(result.inserted_id)}
