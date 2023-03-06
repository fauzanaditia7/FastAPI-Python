from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from tinydb import TinyDB
import json

app = FastAPI()
database = TinyDB("./db.json")

class User(BaseModel):
    id: Optional[int] = Field(default=0)
    name: str

@app.route("/")
async def index(request: Request):
    return {
        "message": "Index Route",
        "status": 200,
        "success": True
    }

@app.post("/user")
async def create_user(user: User):
    d = json.loads(user.json())
    database.insert(d)
    return {
        "message": "Success create new user",
        "status": 200,
        "success": True,
        "user": user.dict()
    }