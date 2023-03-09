from uuid import UUID
from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tinydb import TinyDB, Query
from utils import JSONResponse, User
import json

app = FastAPI()
database = TinyDB("./db.json", indent=4)
Q = Query()


@app.get("/")
async def index(_: Request):
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
async def get_user(id: UUID):
    id = str(id)
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
