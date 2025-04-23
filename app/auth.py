from fastapi import FastAPI, Form, HTTPException
from pymongo import MongoClient
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nkguru.vercel.app/"],  # Your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
users_collection = db["users"]

@app.post("/signup")
async def signup(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    city: str = Form(...),
    zip: str = Form(...),
    password: str = Form(...)
):
    hashed_pw = hash_password(password)

    user_data = {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "address": address,
        "city": city,
        "zip": zip,
        "password": hashed_pw
    }
    users_collection.insert_one(user_data)
    return {"message": "User created successfully!"}

# 🔥 NEW LOGIN ROUTE 🔥
from fastapi import Form, Request

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"email": email})

    if not user or not verify_password(password, user["password"]):
        return {"message": "Invalid email or password"}

    # Login success
    response = RedirectResponse(url="/dashboard", status_code=302)
    return response

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    return response
