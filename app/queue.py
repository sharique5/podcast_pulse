import rq
from redis import Redis

download_queue: rq.Queue = rq.Queue("download", connection=Redis())
transcript_queue: rq.Queue = rq.Queue("transcript", connection=Redis())
summarize_queue: rq.Queue = rq.Queue("summarize", connection=Redis())
mailer_queue: rq.Queue = rq.Queue("mailer", connection=Redis())
