import requests
import os
import io

ELEVEN_LABS_API_KEY = "sk_2af65ef7c06ac45a924554afdef2ed8a7a2b62646715f1dc"  # Or hard-code temporarily
ELEVEN_LABS_VOICE_ID = "6F5Zhi321D3Oq7v1oNT4"  # Replace with your real voice ID

def query_elevenlabs(text: str) -> io.BytesIO:
    if not ELEVEN_LABS_API_KEY:
        raise Exception("Missing Eleven Labs API key")

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_LABS_VOICE_ID}"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Eleven Labs API error {response.status_code}: {response.text}")

    return io.BytesIO(response.content)
