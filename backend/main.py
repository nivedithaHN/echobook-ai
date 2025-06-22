"""
This is the main file for the Echobook AI API.
It contains the FastAPI app and the routes for the API.
"""

import asyncio
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import router
from backend.services import get_valid_tts_voices

# Load environment variables from .env file
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting Echobook AI API...")

    # Start voice caching in background
    async def cache_voices_background():
        try:
            print("Caching voices in background...")
            await asyncio.to_thread(get_valid_tts_voices)
            print("Voice cache loaded.")
        except Exception as e:
            print(f"Failed to cache voices in background: {e}")

    # Start background task
    task = asyncio.create_task(cache_voices_background())

    yield

    # Shutdown logic
    if not task.done():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="Echobook AI",
    description="Echobook AI - Convert books to expressive audio using voice cloning and synthetic voices",
    version="0.1.0",
    lifespan=lifespan,
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
