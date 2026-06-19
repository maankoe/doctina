from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from dataclasses import dataclass
import hashlib
from datetime import datetime, timedelta

SECRET = "THE_SECRET"

@dataclass
class User:
    user_id: str
    password: str
    resources: set[str]

RESOURCES = {"a", "b", "c", "d", "e"}
USER_DB = {
    "the_user": User("the_user", "their_password", {"a", "b", "c"}),
    "another_user": User("another_user", "password", {"a"})
}
TOKEN_LIFETIME = 1

class AuthenticateInput(BaseModel):
    user_id: str
    password: str

class AuthenticateResponse(BaseModel):
    status: str
    token: str | None 

class AuthorizeInput(BaseModel):
    token: str
    resources: list[str] = None

class AuthorizeResponse(BaseModel):
    status: str

@dataclass
class Token:
    user_id: str
    created_at: datetime
    lifetime: int

    def is_expired(self) -> bool:
        return self.created_at + timedelta(seconds=int(self.lifetime)) < datetime.now()

    @classmethod
    def from_str(cls, token: str) -> "Token":
        user_id, created_at, lifetime = token.split("#")
        return cls(
                user_id=user_id, 
                created_at=datetime.fromisoformat(created_at), 
                lifetime=int(lifetime),
        )

    def __str__(self):
        return f"{self.user_id}#{self.created_at.isoformat()}#{self.lifetime}"


def sign(token: str) -> str:
    return hashlib.md5(f"{SECRET}{token}".encode("utf-8")).hexdigest()

def generate_token(user_id: str) -> str:
    token = Token(
            user_id=user_id,
            created_at=datetime.now(),
            lifetime=TOKEN_LIFETIME,
    )
    return f"{sign(token)}#{token}"


app = FastAPI()

@app.post("/authenticate")
async def authenticate(input: AuthenticateInput):
    if input.user_id not in USER_DB:
        return AuthenticateResponse(user_id="user_id", status="UnknownUser", token=None)
    if input.password != USER_DB[input.user_id].password:
        return AuthenticateResponse(user_id=input.user_id, status="Unauthenticated", token=None)
    return AuthenticateResponse(
            status="Authenticated",
            token=generate_token(input.user_id)
    )

@app.post("/authorize")
async def authorize(input: AuthorizeInput):
    signature, raw_token = input.token.split("#", 1)
    token = Token.from_str(raw_token)
    if token.user_id not in USER_DB:
        return AuthorizeResponse(status="UnknownUser")
    if signature != sign(token):
        return AuthorizeResponse(status="Unauthorized: invalid token")
    user_resources = USER_DB[token.user_id].resources
    if input.resources is None and user_resources != RESOURCES \
            or set(input.resources) > set(user_resources):
        return AuthorizeResponse(status="Unauthorized: insufficient access")
    if token.is_expired():
        return AuthorizeResponse(status="Unauthorized: token expired")
    return AuthorizeResponse(status="Authorized")


if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="localhost", port=8000)
    

