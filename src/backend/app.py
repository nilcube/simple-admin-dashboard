from typing import Annotated
from db import DbWrapper
from models import UserCredential, User
from fastapi import FastAPI, HTTPException, status, responses, Response, Cookie

app = FastAPI()


def verify_token(token: str | None) -> User:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token"
        )
    user = DbWrapper.get_user_by_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return user


@app.get("/", response_class=responses.HTMLResponse)
def home():
    return "Home Page"

@app.post("/login")
def login(credentials: UserCredential, response: Response):
    user = DbWrapper.verify_credential(credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Worng user or password"
        )
    token = DbWrapper.create_new_cookies(user)
    response.set_cookie(key="session_id", value=token)
    return {"message":"Cookie set"}

@app.get("/me")
def add_user(session_id: Annotated[str | None, Cookie()] = None):
    user_details = verify_token(session_id).model_dump()
    user_details.pop("password", "")
    return user_details

if __name__ == "__main__":
    pass
