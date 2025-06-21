"""
This is the main file for the Echobook AI API.
It contains the FastAPI app and the routes for the API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router

app = FastAPI(
    title="Echobook AI",
    description="Echobook AI - Convert books to expressive audio using voice cloning and synthetic voices",
    version="0.1.0",
)

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(router)
