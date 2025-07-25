# In main/custom_logic/api.py

from fastapi import FastAPI
from .data_fetcher import get_results
from .schemas import Result

app = FastAPI()

# This will now correctly handle requests to /api/
@app.get("/")
def root():
    return {"Message": "This is Root in Result api"}

# This will now correctly handle requests to /api/results
@app.get("/results")
def results():
    results = get_results()
    return results
