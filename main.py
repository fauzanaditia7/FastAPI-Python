from contextlib import asynccontextmanager
from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query
from utils import JSONResponse
import json

database = TinyDB("./db.json", indent=4)
Q = Query()


@asynccontextmanager
async def lifespan(a: FastAPI):
    app.state.users = [user for user in database.all()]
    yield
    app.state.users.clear()


app = FastAPI(lifespan=lifespan)


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    joinDate: datetime = Field(default_factory=datetime.now)
    isAdmin: bool = Field(default=False)


@app.get("/")
async def index(request: Request):
    return {"message": "Index Route", "status": 200, "success": True}


@app.post("/user")
async def create_user(user: User):
    d = json.loads(user.json())
    database.insert(d)
    return {
        "message": "Success create new user",
        "status": 200,
        "success": True,
        "user": user.dict(),
    }


@app.get("/user")
async def get_user(id: int):
    if not database.contains(Q.id == id):
        return JSONResponse(
            {
                "message": "User not found id : %s" % id,
                "status": 404,
                "success": False,
            },
            status_code=404,
        )
    return {"user": database.search(Q.id == id)[0], "status": 200}


@app.get("/users", response_model=List[User])
async def getUsers():
    return JSONResponse([user for user in database.all()])
