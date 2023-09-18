import redis
import os

con = ""  

def load_redis_config():
    redis_url = os.getenv("REDIS_URL")
    global con
    con = redis.Redis(redis_url)

def is_transcription_running():
    return con.get("TRANSCRIPT_INPROGRESS") == True

def set_transcription_status(val):
    con.set("TRANSCRIPT_INPROGRESS", val)

def is_summarization_running():
    return con.get("SUMMARY_INPROGRESS") == True

def set_summary_status(val):
    con.set("SUMMARY_INPROGRESS", val)
