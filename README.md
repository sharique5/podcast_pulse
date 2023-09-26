# Podcast Pulse

<img src="https://techcrunch.com/wp-content/uploads/2019/02/podcast-mic-blue.png"/>

## Architecure

<img src="https://github.com/sharique5/podcast_pulse/assets/26196076/43002852-69f8-490d-93d3-44fe8386b7c5"/>

## How to run docker

- Make sure you have installed `docker` and `docker-compose`
- Run `docker-compose up -d`
- Go to localhost/
- For local change port to 8000 in docker-compose.yml

## Setup

- Install FFMPEG on your system
- Install Redis on your system
- Make sure you are using Python3
- Git clone the repo
- Run `pip install -r requirements.txt` inside the root dir
- Run the 4 workers (download, transcript, summary, email) in different terminal window using below commands

```sh
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
rq worker download
```

```sh
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
rq worker transcript
```

```sh
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
rq worker summarize
```

```sh
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
rq worker mailer
```

- Now to run the app server

```
uvicorn app.main:app --reload
```
