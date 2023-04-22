from fastapi import FastAPI
from pydantic import BaseModel
from .auth import router as auth_router
from fastapi_sqlalchemy import DBSessionMiddleware, db
import os
from dotenv import load_dotenv
load_dotenv('.env')

app = FastAPI()
app.include_router(auth_router.app, prefix='/api/v1')
app.add_middleware(DBSessionMiddleware, db_url=os.environ.get('DATABASE_URL'))

@app.get('/')
def home():
    dict = {}
    data = []
    for i in range(10):
        data.append({'Hello' : i})
    dict["data"] = data
    return dict