from fastapi import FastAPI
from app.auth import router as auth_router

app = FastAPI()

# Include the authentication routes (signup)
app.include_router(auth_router)
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI App!"}
