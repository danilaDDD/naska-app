from pydantic import BaseModel, model_validator
from typing import Any, Optional


class PutUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

    @model_validator(mode="after")
    def check_email_unique(self, info: Any) -> "PutUserRequest":
        users = info.context.get("users", []) if info.context else []
        if self.email and any(u.email == self.email for u in users):
            raise ValueError("Email already exists")
        return self


class User(BaseModel):
    id: int
    name: str
    email: str = ""

    @model_validator(mode="after")
    def check_email_unique(self, info: Any) -> "User":
        users = info.context.get("users", []) if info.context else []
        if self.email and any(u.email == self.email for u in users):
            raise ValueError("Email already exists")
        return self