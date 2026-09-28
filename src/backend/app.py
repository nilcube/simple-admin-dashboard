from typing import Annotated
from db import DbWrapper
from models import UserCredential, User
from fastapi import FastAPI, HTTPException, status, responses, Response, Cookie
from fastapi.staticfiles import StaticFiles

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

def verify_admin(token: str|None) -> User:
    user = verify_token(token)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You're not an admin"
        )


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


@app.get("/list-users")
def list_all_users(session_id: Annotated[str | None, Cookie()] = None):
    verify_admin(session_id)
    return DbWrapper.get_all_users()


@app.post("/create-user")
def create_user(
    user: User,
    session_id: Annotated[str | None, Cookie()] = None,
):
    verify_admin(session_id)
    if not DbWrapper.add_user(user):
        raise HTTPException(
            status_code=409,
            detail="Username is already at use"
        )
    return responses.JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User is created"}
    )




app.mount("/static", StaticFiles(directory="static"))
