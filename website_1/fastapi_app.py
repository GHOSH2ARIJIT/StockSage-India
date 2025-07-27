from fastapi import FastAPI,Request
from pydantic import BaseModel
from mongodb import db  # your mongo client
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

fastapi_app = FastAPI()
templates = Jinja2Templates(directory="templates/webpage_1")

client = MongoClient('mongodb://localhost:27017/')
db = client['stocksage_db']
footer_collection = db['footer_data']

class Prediction(BaseModel):
    company: str
    prediction: str
    confidence: float

@fastapi_app.post("/fastapi/save/")
async def save_data(data: Prediction):
    # Convert Pydantic object to dict
    result = await db.predictions.insert_one(data.dict())
    return {"inserted_id": str(result.inserted_id)}



@fastapi_app.get("/api/footer/")
def get_footer_data():
    footer_data = footer_collection.find_one({}, {'_id': 0})
    return footer_data

