from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.elevenlabs_api import generate_speech
from app.cartesia_api import query_cartesia
import io

router = APIRouter()

@router.get("/speak")
def speak_text(text: str, voice_id: str = "default"):
    try:
        audio_data = generate_speech(text, voice_id)
        return StreamingResponse(io.BytesIO(audio_data), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cartesia")
def ask_cartesia(prompt: str):
    try:
        result = query_cartesia(prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
