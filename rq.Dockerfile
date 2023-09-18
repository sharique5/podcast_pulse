FROM ubuntu:20.04

# ffmpeg needed for services
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9 pip
RUN apt-get install -y ffmpeg

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt && rm -rf /root/.cache/pip

#
COPY ./app /code/app
COPY ./.env /code/.env

CMD ["rq", "worker"]