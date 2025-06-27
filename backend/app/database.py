import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.bio_d_scan
bee_data_collection = database.get_collection("bee_data")

# Test database connection
async def test_connection():
    try:
        await client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas!")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return False