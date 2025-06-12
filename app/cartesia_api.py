import requests
import os

CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
BASE_URL = "https://api.cartesia.ai/v1"

def query_cartesia(prompt: str) -> dict:
    headers = {
        "Authorization": f"Bearer {CARTESIA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"prompt": prompt}
    response = requests.post(f"{BASE_URL}/query", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
