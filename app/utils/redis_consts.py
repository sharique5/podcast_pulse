import redis
import os

redis_url = os.getenv("REDIS_URL")
con = redis.Redis(redis_url, decode_responses=True)
print(con)

def is_transcription_running():
    global con
    return con.get("TRANSCRIPT_INPROGRESS") == "True"

def set_transcription_status(val):
    global con
    con.set("TRANSCRIPT_INPROGRESS", val)

def is_summarization_running():
    global con
    return con.get("SUMMARY_INPROGRESS") == "True"

def set_summary_status(val):
    global con
    con.set("SUMMARY_INPROGRESS", val)
