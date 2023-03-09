from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from starlette.responses import Response
import typing
import json


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    joinDate: datetime = Field(default_factory=datetime.now)
    isAdmin: bool = False


class JSONResponse(Response):
    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(",", ": "),
        ).encode("utf-8")
