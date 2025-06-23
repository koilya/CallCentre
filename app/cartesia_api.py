import requests #pip install
import os
import io

CARTESIA_API_KEY = "sk_car_AXuY2dCW9H8TNVpyt7rH4B"
url = "https://api.cartesia.ai/tts/bytes"

def query_cartesia(transcript: str) -> io.BytesIO:
    headers = {
        "Cartesia-Version": "2025-04-16",
        "Authorization": f"Bearer {CARTESIA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {"model_id": "sonic-2",
               "transcript": transcript,
                 "voice":{ "mode": "id",
        "id": "694f9389-aac1-45b6-b726-9d9369183238"
        },
        "output_format": {
        "container": "mp3",
        "bit_rate": 128000,
        "sample_rate": 44100
        },
        "language": "en"
        }
    
    print("Sending request to Cartesia...")
    print("Headers:", headers)
    print("Payload:", payload)

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Cartesia response status:", response.status_code)

        if response.status_code == 200:
            # Save to file for local use/debug
            with open("output.mp3", "wb") as f:
                f.write(response.content)
            print("Audio saved to output.mp3")

            # Also return as BytesIO for in-memory use
            return io.BytesIO(response.content)
        else:
            print("Cartesia API Error:", response.status_code)
            print("Response body:", response.text)
            raise Exception(f"Cartesia API Error {response.status_code}: {response.text}")

    except Exception as e:
        print("Exception while calling Cartesia API:", str(e))
        raise