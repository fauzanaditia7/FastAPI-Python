from typing import List
from uuid import UUID
from fastapi import APIRouter
from utils import User, Q, database, JSONResponse
import json


api = APIRouter(prefix="/api", tags=["API"])


@api.post("/user")
async def create_user(user: User):
    d = json.loads(user.json())
    database.insert(d)
    return {
        "message": "Success create new user",
        "status": 200,
        "success": True,
        "user": user.dict(),
    }


@api.get("/user")
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


@api.get("/users", response_model=List[User])
async def getUsers():
    return JSONResponse([user for user in database.all()])
