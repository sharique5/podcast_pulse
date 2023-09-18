import rq
import os
from redis import Redis

redis_url = os.getenv("REDIS_URL")

download_queue: rq.Queue = rq.Queue("download", connection=Redis(redis_url))
transcript_queue: rq.Queue = rq.Queue("transcript", connection=Redis(redis_url))
summarize_queue: rq.Queue = rq.Queue("summarize", connection=Redis(redis_url))
mailer_queue: rq.Queue = rq.Queue("mailer", connection=Redis(redis_url))
