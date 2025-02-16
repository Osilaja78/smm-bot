"""Main module for running FastAPI app"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import models
from api.database import engine
from api.routers import tiktok, youtube
import uvicorn


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://sketch-sync.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database migration
models.Base.metadata.create_all(bind=engine)


@app.get("/health")
async def health():
    """Check the status of the API"""

    return {'status': 'Running...'}


@app.get("/")
async def root():
    """Root route of the API"""

    return {"message": "Welcome to the social media manager (SMM) API!"}


# Include routes from other router files
app.include_router(tiktok.router)
app.include_router(youtube.router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)