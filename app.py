from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow the artifact to call this from any origin

ESV_KEY = "131cf9d78015127851f546e00606324f2c7b2582"
ESV_AUDIO_URL = "https://api.esv.org/v3/passage/audio/"

@app.route("/")
def index():
    return {"status": "ok", "service": "TPC ESV Audio Proxy"}

@app.route("/audio")
def audio():
    q = request.args.get("q", "").strip()
    if not q:
        return {"error": "Missing 'q' parameter. Usage: /audio?q=Genesis+1"}, 400

    try:
        resp = requests.get(
            ESV_AUDIO_URL,
            params={"q": q},
            headers={"Authorization": f"Token {ESV_KEY}"},
            allow_redirects=True,
            timeout=30,
        )
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"ESV API request failed: {str(e)}"}, 502

    return Response(
        resp.content,
        content_type="audio/mpeg",
        headers={
            "Cache-Control": "public, max-age=86400",  # Cache MP3s for 24hrs
            "Accept-Ranges": "bytes",
        },
    )

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
