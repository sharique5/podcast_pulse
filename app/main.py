import os
import traceback
import shortuuid
import psycopg2
from dotenv import load_dotenv
from fastapi import Request, FastAPI
from rq import Retry
from app.queue import download_queue
from app.core import downloader, transcribe
from app.workers.download import start_download_work
from app.db import db_client


# dont move this down
load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "🚀"}


# @app.get("/test/{message}")
# def test(message: str):
#     print(download_queue.count)
#     download_queue.enqueue(download.start_download_work, message, retry=Retry(max=3))
#     return {"testing": message}

@app.post("/summary")
async def summarizeAndSendMail(request: Request):
    body = None
    try:
        body = await request.json();
    except Exception:
        body = {}
        print("Exception happened while parsing request body")


    podcast_url = body.get("url", None);
    email = body.get("email", None)

    if podcast_url is None or email is None:
        response = {
            "success": False,
            "message": "Invalid request body provided",
            "data": {}
        }

        return response
    
    # prepare request body to send on download queue
    file_id = shortuuid.uuid()
    is_insertion_failed = False
    try:
        podcast_details_insert_query = """INSERT INTO podcast_details (podcast_url, email, file_id) VALUES (%s,%s,%s) RETURNING id;"""
        podcast_details_to_insert = (podcast_url, email, file_id)
        cursor = db_client.cursor()
        cursor.execute(podcast_details_insert_query, podcast_details_to_insert)
        uid = cursor.fetchone()[0]

        # commit changes and then close the cursor
        db_client.commit()
        print("PostgreSQL successfully inserted")
    except (Exception, psycopg2.Error) as error:
        print(traceback.format_exc())
        print("Failed to insert record into podcast_details table", error)
        is_insertion_failed = True
    finally:
        # closing database connection.
        if db_client:
            cursor.close()
            if is_insertion_failed:
                response = {
                    "success": False,
                    "message": "Failed to process the request, check DB",
                    "data": {}
                }
                return response
    
    # i am passing this data packet to download queue
    download_task_dict = {
        "uid": uid,
        "url": podcast_url,
        "file_id": file_id
    }
        
    print("Sending to queue =  {}".format(download_task_dict))
    # send data to download queue
    download_queue.enqueue(start_download_work, download_task_dict)
    return download_task_dict

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
    with open(transcript_file_path, "r") as file:
        content = file.read()
        
    # Print the content
    print(content)
    return {"transcript": content, "success": True}
