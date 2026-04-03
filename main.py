from fastapi import FastAPI, HTTPException
import re

app = FastAPI()

@app.get("/transcript")
def get_transcript(url: str):
    video_id = extract_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        text = " ".join([t.text for t in transcript])
        return {"video_id": video_id, "transcript": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_id(url: str):
    match = re.search(r"(?:v=|youtu\.be/|shorts/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None
