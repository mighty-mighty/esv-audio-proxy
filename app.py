from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="static")
CORS(app)

ESV_KEY = os.environ.get("ESV_API_KEY", "131cf9d78015127851f546e00606324f2c7b2582")
ESV_AUDIO_URL = "https://api.esv.org/v3/passage/audio/"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/audio")
def audio():
    q = request.args.get("q", "").strip()
    if not q:
        return {"error": "Missing 'q' parameter"}, 400
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
        return {"error": str(e)}, 502
    return Response(
        resp.content,
        content_type="audio/mpeg",
        headers={"Cache-Control": "public, max-age=86400"},
    )

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
