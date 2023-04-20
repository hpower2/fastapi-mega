from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def home():
    dict = {}
    data = []
    for i in range(10):
        data.append({'Hello' : i})
    dict["data"] = data
    return dict