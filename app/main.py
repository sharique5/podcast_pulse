from dotenv import load_dotenv
from fastapi import Request, FastAPI
from app.core import downloader, transcribe
import traceback

load_dotenv()
app = FastAPI()


@app.get("/")
def root():
    return {"message": "🚀"}


@app.post("/transcribe")
async def transcribeAudio(request: Request):
    try:
        body = await request.json()
        podcast_url = body["url"]
        if podcast_url is None:
            return {"message": "Podcast URL not provided", "success": False}
        
        downloaded_file_path = await downloader.download_youtube_podcast(podcast_url)
        if downloaded_file_path is None:
            return {"message": "Failed while fetching audio from the URL"}
        
        print("Downloaded path is {}".format(downloaded_file_path))
        complete_transcript = transcribe.speech_continuous_recognition(downloaded_file_path)
        print("Length of transcript is {}".format(len(complete_transcript)))
        # perform transcription now
        return {"message": downloaded_file_path, "success": True}
    except Exception:
        print(traceback.format_exc())
        return {"message": "Error occured while transcibing audio"}