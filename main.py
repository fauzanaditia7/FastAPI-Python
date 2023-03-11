from fastapi import FastAPI, Request
from api_router import api

app = FastAPI()


@app.get("/")
async def index(_: Request):
    return {"message": "Index Route", "status": 200, "success": True}


app.include_router(api)
