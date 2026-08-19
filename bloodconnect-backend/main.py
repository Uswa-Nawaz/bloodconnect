from fastapi import FastAPI

app = FastAPI()

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