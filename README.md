# TPC ESV Audio Proxy

A tiny Flask server that proxies the ESV Bible audio API, adding authentication server-side so browser apps can play MP3s without CORS issues.

## What it does

- Receives requests like `/audio?q=Genesis+1`
- Calls the ESV API with your auth token
- Returns the MP3 directly to the browser
- Caches responses for 24 hours

## Deploy to Railway

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) and sign in with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select this repo
5. Railway auto-detects Python and deploys
6. Once live, go to **Settings** → **Networking** → **Generate Domain**
7. Your URL will be something like `https://esv-audio-proxy-production.up.railway.app`

## Test it

```
curl https://YOUR-URL.up.railway.app/audio?q=John+3:16 > test.mp3
```

## Endpoints

- `GET /` — Status check
- `GET /audio?q=Genesis+1` — Returns MP3 audio for the passage
- `GET /health` — Health check

## Local development

```bash
pip install -r requirements.txt
python app.py
# Visit http://localhost:8080/audio?q=Psalm+23
```
