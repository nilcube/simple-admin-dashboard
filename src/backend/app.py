from typing import Annotated

from fastapi.param_functions import Depends
from db import DbWrapper
from models import Note, UserCredential, User
from fastapi import FastAPI, HTTPException, status, responses, Response, Cookie
from fastapi.staticfiles import StaticFiles

app = FastAPI()


def verify_token(session_id: Annotated[str | None, Cookie()] = None) -> User:
    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token"
        )
    user = DbWrapper.get_user_by_token(session_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return user

def verify_admin(session_id: Annotated[str | None, Cookie()] = None) -> User:
    user = verify_token(session_id)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You're not an admin"
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
def add_user(user = Depends(verify_token)):
    user_details = user.model_dump()
    user_details.pop("password", "")
    return user_details


@app.get("/list-users", dependencies=[Depends(verify_admin)])
def list_all_users():
    return DbWrapper.get_all_users()


@app.post("/create-user", dependencies=[Depends(verify_admin)])
def create_user(
    user: User,
):
    if not DbWrapper.add_user(user):
        raise HTTPException(
            status_code=409,
            detail="Username is already at use"
        )
    return responses.JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User is created"}
    )

@app.post("/note")
def new_note(
    note: Note,
    user: User = Depends(verify_token)
):
    DbWrapper.new_note(note, user.id)






app.mount("/static", StaticFiles(directory="static"))
