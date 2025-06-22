from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services import TTSVoices, generate_tts, get_valid_tts_voices
from backend.utils.config import SERVER_ERROR_STATUS_CODE

router = APIRouter()


class GenerateAudioRequest(BaseModel):
    """
    Request body for generating audio from text using Resemble AI API.

    Args:
        text: The text to generate audio from.
        voice_id: The ID of the voice to use for the audio.
        output_format: The format of the audio to generate.
        title: The title of the audio.
    """

    text: str
    voice_id: str
    output_format: str = "mp3"
    title: str = "TTS"


@router.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to the Echobook AI API"}


@router.post("/generate-audio")
def generate_audio(request: GenerateAudioRequest) -> dict[str, str]:
    """
    Generate audio from text using Resemble AI API.

    Args:
        request: The request containing text, voice_id, output_format, and title
    """

    try:
        audio_path = generate_tts(
            request.text, request.voice_id, request.output_format, request.title
        )
        return {"audio_path": audio_path}
    except Exception as e:
        raise HTTPException(
            status_code=SERVER_ERROR_STATUS_CODE, detail={"error": str(e)}
        )


@router.get("/tts-voices")
def get_tts_voices() -> dict[str, TTSVoices]:
    """
    Get the list of voices available for the Resemble AI API.
    """

    try:
        voices = get_valid_tts_voices()
        return voices
    except Exception as e:
        raise HTTPException(
            status_code=SERVER_ERROR_STATUS_CODE, detail={"error": str(e)}
        )
