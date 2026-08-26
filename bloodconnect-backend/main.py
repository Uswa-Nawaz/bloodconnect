from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from db import engine, get_db
from repository import UserRepository
from service import AuthService
from schemas import UserSignupRequest, UserLoginRequest, UserResponse

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend is running"}

from db import engine
from sqlalchemy import text

@app.get("/test-db")
def test_db():
    print("TEST ROUTE STARTED")

    with engine.connect() as connection:
        print("CONNECTED TO DATABASE")

        result = connection.execute(text("SELECT 1"))
        print("QUERY EXECUTED:", result.scalar())

    print("TEST ROUTE FINISHED")

    return {"message": "Database connected successfully"}

@app.post("/signup", response_model=UserResponse)
def signup(signup_data: UserSignupRequest, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    service = AuthService(repository)
    try:
        new_user = service.signup(signup_data)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login", response_model=UserResponse)
def login(login_data: UserLoginRequest, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    service = AuthService(repository)
    try:
        user = service.login(login_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))