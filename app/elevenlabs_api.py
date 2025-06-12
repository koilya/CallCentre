import requests
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")  # Or hard-code temporarily
BASE_URL = "https://api.elevenlabs.io/v1"

def generate_speech(text: str, voice_id: str = "default") -> bytes:
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {"stability": 0.75, "similarity_boost": 0.75}
    }
    response = requests.post(f"{BASE_URL}/text-to-speech/{voice_id}", json=payload, headers=headers)
    response.raise_for_status()
    return response.content  # This is audio data
