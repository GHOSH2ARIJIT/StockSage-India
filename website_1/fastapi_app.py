from fastapi import FastAPI

fastapi_app  = FastAPI()

@fastapi_app.get("/fastapi/hello")
def read_root():
    return {"message": "Hello from FastAPI: Arijit....."}