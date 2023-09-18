# Podcast Pulse

## Setup

- Install FFMPEG on your system
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
