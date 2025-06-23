from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from pydantic import BaseModel
import io
from app.cartesia_api import query_cartesia  # your function returning io.BytesIO
from app.elevenlabs_api import query_elevenlabs 

app = FastAPI()

class TextRequest(BaseModel):
    transcript: str

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
      <head>
        <title>TTS Services</title>
      </head>
      <body>
        <h2>Enter text to convert to speech</h2>
        <textarea id="transcript" rows="4" cols="50"></textarea><br><br>
        <button onclick="sendText('cartesia')">Speak with Cartesia</button>
        <button onclick="sendText('elevenlabs')">Speak with Eleven Labs</button>
        <p id="status"></p>
        <audio id="player" controls></audio>

        <script>
          async function sendText(engine) {
            const text = document.getElementById('transcript').value;
            const status = document.getElementById('status');
            const player = document.getElementById('player');

            if (!text.trim()) {
              status.textContent = "Please enter some text.";
              return;
            }

            status.textContent = "Calling " + engine + " API...";

            let endpoint = '';
            if (engine === 'cartesia') {
              endpoint = '/speak';
            } else if (engine === 'elevenlabs') {
              endpoint = '/speak-elevenlabs';
            }

            try {
              const response = await fetch(endpoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({transcript: text})
              });

              if (!response.ok) {
                const error = await response.text();
                status.textContent = "Error: " + error;
                return;
              }

              const blob = await response.blob();
              const url = URL.createObjectURL(blob);
              player.src = url;
              player.play();

              status.textContent = "Playing audio!";
            } catch (err) {
              status.textContent = "Fetch error: " + err.message;
            }
          }
        </script>
      </body>
    </html>
    """


@app.post("/speak")
async def speak(req: TextRequest):
    try:
        audio_stream = query_cartesia(req.transcript)
        audio_stream.seek(0)
        return StreamingResponse(audio_stream, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speak-elevenlabs")
async def speak_elevenlabs(req: TextRequest):
    try:
        audio_stream = query_elevenlabs(req.transcript)
        audio_stream.seek(0)
        return StreamingResponse(audio_stream, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eleven Labs error: {e}")