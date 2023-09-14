from dotenv import load_dotenv
from fastapi import Request, FastAPI
from app.core import downloader, transcribe
import traceback
import os

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
        transcript_file_name = os.path.splitext(os.path.basename(downloaded_file_path))[0] + ".txt"
        curr_dir = os.path.dirname(os.path.abspath(__file__)) 
        transcript_file_path = os.path.normpath(os.path.join(curr_dir, "../", "transcripts", transcript_file_name))
        await transcribe.speech_continuous_recognition(downloaded_file_path, transcript_file_path)
        # perform transcription now
        return {"message": transcript_file_path, "success": True}
    except Exception:
        print(traceback.format_exc())
        return {"message": "Error occured while transcibing audio"}
    

@app.get("/show/transcript/{transcript_id}")
def show_transcript(transcript_id):
    curr_dir = os.path.dirname(os.path.abspath(__file__)) 
    transcript_file_path = os.path.normpath(os.path.join(curr_dir, "../", "transcripts", transcript_id + ".txt"))
    if os.path.isfile(transcript_file_path):
        with open(transcript_file_path, "r") as file:
            content = file.read()
        # Print the content
        print(content)
        return {"transcript": content, "success": True}
    else:
        return {"transcript": "Not Found!", "success": False}
