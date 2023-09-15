import requests
from datetime import datetime, timedelta
import time
from rqs import queue2, queue3, a

def print_task(seconds):
    print(a)
    print("Starting task")
    for num in range(seconds):
        print(num, ". Hello World!")
        time.sleep(1)
    print("Task completed")
    a += 1
    if a < 2:
        raise Exception("Exception hello {}".format(a))
    # queue = rq.Queue(connection=Redis())
    queue2.enqueue(print_numbers, 5)


def print_numbers(seconds):
    print("Starting num task")
    for num in range(seconds):
        print(num)
        time.sleep(1)
    print("Task to print_numbers completed")
    queue3.enqueue(count_words_at_url, "http://example.com")

def count_words_at_url(url):
    # resp = requests.get(url)
    print("len")
    print(len(url))
    return len(url)

def say_hello():
    return "Hello world!"
