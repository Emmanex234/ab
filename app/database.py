from motor.motor_asyncio import AsyncIOMotorClient
import os

# Load MongoDB URL from environment variable or use default
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)

# Select the database and collection
db = client["auth_db"]  # Use your database name
users_collection = db["users"]  # Use your collection name
