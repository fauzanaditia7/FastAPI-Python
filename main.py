from datetime import date, datetime
from typing import Optional, Union
from uuid import UUID, uuid4
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import UUID4, BaseModel, Field, validator
from tinydb import TinyDB, Query
import json

app = FastAPI()
database = TinyDB("./db.json", indent=4)
Q = Query()


class User(BaseModel):
    id: UUID | UUID4 = Field(default_factory=uuid4)
    name: str
    joinDate: date = Field(default_factory=datetime.now)
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
