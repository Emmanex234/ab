from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# ✅ Setup CORS (allow only frontend port)
origins = [
    "http://127.0.0.1:5500",  # Your frontend origin
    "http://localhost:5500",  # Optional, for localhost use
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
users_collection = db["users"]

# Password helpers
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 📝 Signup Route
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

# 🔐 Login Route
@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    return RedirectResponse(url="/dashboard", status_code=303)

# 🖥 Dashboard
templates = Jinja2Templates(directory="templates")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
