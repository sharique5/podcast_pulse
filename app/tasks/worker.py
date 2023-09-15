# from redis import Redis
# from rq import Queue
# from datetime import timedelta
# from util import count_words_at_url, say_hello

# q = Queue(connection=Redis())


# result = q.enqueue(count_words_at_url, 'http://nvie.com')
# # Schedule job to run at 9:15, October 10th
# # job = q.enqueue(say_hello)

# # # Schedule job to be run in 10 seconds
# # job = q.enqueue_in(timedelta(seconds=10), say_hello)

from datetime import datetime, timedelta
import time
from redis import Redis
from rqs import queue
from rq import Retry


def queue_tasks():
    queue.enqueue("our_utils.print_task", 5, retry=Retry(max=3))
    # queue.enqueue_in(timedelta(seconds=10), "our_utils.print_numbers", 5)

def main():
    queue_tasks()

if __name__ == "__main__":
    main()


# - download -> file -> transc
# - transc -> ... -> schedule(summary) db
# - summary -> ... -> email db
# - email -> ... -> db