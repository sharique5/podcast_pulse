import rq
from redis import Redis

queue = rq.Queue("default", connection=Redis())
queue2 = rq.Queue("low", connection=Redis())
queue3 = rq.Queue("download", connection=Redis())
