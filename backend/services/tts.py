"""
This module sends a TTS request to Resemble AI API and saves the generated audio.
"""

import base64
import os
from uuid import uuid4

import requests
from dotenv import load_dotenv

from backend.services.config import (
    RESEMBLE_API_BASE,
    SUCCESS_STATUS_CODE,
    TTS_AUDIO_PATH,
)

# Load environment variables from .env file
load_dotenv()

# Get environment variables from .env file
RESEMBLE_API_KEY = os.getenv("RESEMBLE_API_KEY")
RESEMBLE_PROJECT_ID = os.getenv("RESEMBLE_PROJECT_ID")

# Headers for the request to the Resemble AI API
HEADERS = {
    "Authorization": f"Bearer {RESEMBLE_API_KEY}",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip",
}


def generate_tts(
    text: str, voice_id: str, output_format: str = "mp3", title: str = "TTS"
) -> str:
    """
    Generate TTS audio from text using Resemble AI API.

    Args:
        text: The text to generate TTS audio from.
        voice_id: The ID of the voice to use for the TTS audio.
        output_format: The format of the audio to generate.
        title: The title of the TTS audio.

    Returns:
        The path to the generated audio file.
    """

    if not RESEMBLE_API_KEY:
        raise ValueError("RESEMBLE_API_KEY must be set in the environment variables")

    payload = {
        "voice_uuid": voice_id,
        "data": text,
        "title": title,
        "output_format": output_format,
    }

    try:
        response = requests.post(
            url=RESEMBLE_API_BASE, headers=HEADERS, json=payload, timeout=30
        )

        if response.status_code != SUCCESS_STATUS_CODE:
            raise Exception(
                f"Failed to generate TTS from Resemble AI: {response.status_code} {response.text}"
            )

        response_data = response.json()
        audio_base64 = response_data.get("audio_content")

        if not audio_base64:
            raise Exception("No audio content from Resemble AI response")

        audio_binary = base64.b64decode(audio_base64)
        output_path = f"{TTS_AUDIO_PATH}/{uuid4().hex}.{output_format}"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(audio_binary)

        return output_path

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error when calling Resemble AI: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating TTS: {str(e)}")
