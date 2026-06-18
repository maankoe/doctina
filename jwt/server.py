from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from dataclasses import dataclass
import hashlib


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


class AuthenticateInput(BaseModel):
    user_id: str
    password: str

class AuthenticateResponse(BaseModel):
    user_id: str
    status: str
    token: str | None 

class AuthorizeInput(BaseModel):
    user_id: str
    token: str
    resources: list[str] = None

class AuthorizeResponse(BaseModel):
    user_id: str
    status: str

def generate_token(user: User) -> str:
    original = f"TOKEN:{SECRET}:{user.user_id}"
    return hashlib.md5(original.encode("utf-8")).hexdigest()


app = FastAPI()

@app.post("/authenticate")
async def authenticate(input: AuthenticateInput):
    if input.user_id not in USER_DB:
        return AuthenticateResponse(user_id="user_id", status="UnknownUser", token=None)
    if input.password != USER_DB[input.user_id].password:
        return AuthenticateResponse(user_id=input.user_id, status="Unauthenticated", token=None)
    return AuthenticateResponse(
            user_id=input.user_id,
            status="Authenticated",
            token=generate_token(USER_DB[input.user_id])
    )

@app.post("/authorize")
async def authorize(input: AuthorizeInput):
    if input.user_id not in USER_DB:
        return AuthorizeResponse(user_id=input.user_id, status="UnknownUser")
    if input.token != generate_token(USER_DB[input.user_id]):
        return AuthorizeResponse(user_id=input.user_id, status="Unauthorized")
    if input.resources is None and USER_DB[input.user_id].resources != RESOURCES:
        return AuthorizeResponse(user_id=input.user_id, status="Unauthorized")
    if set(input.resources) > set(USER_DB[input.user_id].resources):
        return AuthorizeResponse(user_id=input.user_id, status="Unauthorized")
    return AuthorizeResponse(user_id=input.user_id, status="Authorized")


if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="localhost", port=8000)
    

