from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.database import test_connection
import uvicorn

app = FastAPI(
    title="Bio D Scan API",
    description="Full Stack Bee Hive Data Management with FastAPI",
    version="1.0.0"
)

# CORS middleware to allow React frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Bio D Scan API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    await test_connection()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)