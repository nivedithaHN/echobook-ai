"""
This module sends a TTS request to Resemble AI API and saves the generated audio.
It also contains the functions for getting the list of voices available for the Resemble AI API.
"""

import base64
import os
from dataclasses import dataclass
from typing import List
from uuid import uuid4

import requests

from backend.utils.config import (
    RESEMBLE_SYNTHESIZE_API_BASE,
    RESEMBLE_VOICES_API_BASE,
    SUCCESS_STATUS_CODE,
    TTS_AUDIO_PATH,
)

# Get environment variables from environment variables
RESEMBLE_API_KEY = os.getenv("RESEMBLE_API_KEY")


@dataclass
class TTSVoices:
    """TTS Voice data model"""

    uuid: str
    name: str
    status: str
    default_language: str
    voice_type: str
    supported_languages: List[str]
    source: str


# Global cache for TTS voices
TTS_VOICES_CACHE: dict[str, TTSVoices] = {}
# Loading state
VOICES_LOADING = False


def validate_tts_voice(voice_id: str) -> bool:
    """
    Validate if the voice is available for the Resemble AI API.
    """
    return voice_id in TTS_VOICES_CACHE


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

    # Headers for the request to the Resemble AI API
    HEADERS = {
        "Authorization": f"Bearer {RESEMBLE_API_KEY}",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip",
    }

    try:
        # Check if the Resemble API key is set in the environment variables
        if not RESEMBLE_API_KEY:
            raise ValueError(
                "RESEMBLE_API_KEY must be set in the environment variables"
            )
        # Check output format
        if output_format not in ["mp3", "wav"]:
            raise ValueError("Invalid output format")

        # Check if the text is empty
        if not text:
            raise ValueError("Text is empty")

        # Check if the voice is available in the cache
        if not validate_tts_voice(voice_id):
            raise ValueError(f"Voice {voice_id} is not available")

        payload = {
            "voice_uuid": voice_id,
            "data": text,
            "title": title,
            "output_format": output_format,
        }

        response = requests.post(
            url=RESEMBLE_SYNTHESIZE_API_BASE, headers=HEADERS, json=payload, timeout=30
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
    except ValueError as e:
        raise Exception(f"Error generating TTS: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating TTS: {str(e)}")


def get_valid_tts_voices() -> dict[str, TTSVoices]:
    """
    Get the list of voices available for the Resemble AI API.
    """
    # Check global cache
    global TTS_VOICES_CACHE

    if TTS_VOICES_CACHE:
        return TTS_VOICES_CACHE

    # Headers for the request to the Resemble AI API
    HEADERS = {
        "Authorization": f"Bearer {RESEMBLE_API_KEY}",
    }

    try:
        if not RESEMBLE_API_KEY:
            raise ValueError(
                "RESEMBLE_API_KEY must be set in the environment variables"
            )

        all_voices = {}
        current_page = 1

        while True:
            params = {
                "page": current_page,
            }

            paginated_result = requests.get(
                url=RESEMBLE_VOICES_API_BASE, headers=HEADERS, params=params
            )

            if paginated_result.status_code != SUCCESS_STATUS_CODE:
                raise Exception(
                    f"Failed to get voices: {paginated_result.status_code} {paginated_result.text}"
                )

            voices_data = paginated_result.json()

            if not voices_data.get("success"):
                raise Exception(f"Failed to get voices: {voices_data.get('error')}")

            num_pages = voices_data.get("num_pages", 1)

            for voice in voices_data["items"]:
                all_voices[voice["uuid"]] = TTSVoices(
                    uuid=voice["uuid"],
                    name=voice["name"],
                    status=voice["status"],
                    default_language=voice["default_language"],
                    voice_type=voice["voice_type"],
                    supported_languages=voice["supported_languages"],
                    source=voice["source"],
                )

            if current_page >= num_pages:
                break
            current_page += 1

        # Update global cache
        TTS_VOICES_CACHE = all_voices

        return all_voices
    except Exception as e:
        raise Exception(f"Error getting voices: {str(e)}")
