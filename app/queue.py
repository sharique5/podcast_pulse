import rq
import os
from dotenv import load_dotenv
from redis import Redis

load_dotenv()
redis_url: str = os.getenv("REDIS_URL")

download_queue: rq.Queue = rq.Queue("download", connection=Redis(redis_url))
transcript_queue: rq.Queue = rq.Queue("transcript", connection=Redis(redis_url))
summarize_queue: rq.Queue = rq.Queue("summarize", connection=Redis(redis_url))
mailer_queue: rq.Queue = rq.Queue("mailer", connection=Redis(redis_url))
