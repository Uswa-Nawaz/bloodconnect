from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text


from db import engine, get_db
from repository import UserRepository,RequestRepository
from service import AuthService,RequestService
from schemas import UserSignupRequest, UserLoginRequest, UserResponse,RequestCreate, RequestResponse
from typing import List

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://127.0.0.1:5501"],
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

@app.get("/admin/pending-users",  response_model=List[UserResponse])
def get_pending_users(admin_id: int, db: Session = Depends(get_db)): 
        repository = UserRepository(db)
        service = AuthService(repository)
        try:
            service.verify_admin(admin_id)
            return repository.get_pending_users()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

@app.post("/admin/approve/{id}", response_model=UserResponse)
def approve_users(admin_id: int, id: int,  db: Session = Depends(get_db)):
    repository = UserRepository(db)
    service = AuthService(repository)
    try:
        approved_users=service.approve_user(admin_id, id)
        return approved_users
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/admin/reject/{id}", response_model=UserResponse)
def reject_users(admin_id: int, id: int,  db: Session = Depends(get_db)):
    repository = UserRepository(db)
    service = AuthService(repository)
    try:
        rejected_users=service.reject_user(admin_id, id)
        return rejected_users
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/admin/suspend/{id}", response_model=UserResponse)
def suspend_users(admin_id: int, id: int, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    service = AuthService(repository)
    try:
        suspended_user = service.suspend_user(admin_id, id)
        return suspended_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


#----------Request routes--------
@app.post("/requests", response_model=RequestResponse)
def submit_request(user_id: int, request_data: RequestCreate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    request_repository = RequestRepository(db)
    service = RequestService(request_repository, user_repository)
    try:
        new_request = service.submit_request(user_id, request_data)
        return new_request
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/requests/{id}/cancel", response_model=RequestResponse)
def cancel_request(user_id: int, id: int, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    request_repository = RequestRepository(db)
    service = RequestService(request_repository, user_repository)
    try:
        cancelled = service.cancel_request(user_id, id)
        return cancelled
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/requests/my", response_model=List[RequestResponse])
def get_my_requests(user_id: int, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    request_repository = RequestRepository(db)
    service = RequestService(request_repository, user_repository)
    return service.get_my_requests(user_id)