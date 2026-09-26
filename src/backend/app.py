from db import DbWrapper
from models import UserCredential
from fastapi import FastAPI, HTTPException, status, responses, Response

app = FastAPI()


@app.get("/", response_class=responses.HTMLResponse)
def home():
    return "Home Page"

@app.post("/login")
def login(credentials: UserCredential, response: Response):
    user = DbWrapper.verify_credential(credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="worng user or password"
        )
    token = DbWrapper.create_new_cookies(user)
    response.set_cookie(key="session_id", value=token)
    return {"message":"Cookie set"}


if __name__ == "__main__":
    pass
