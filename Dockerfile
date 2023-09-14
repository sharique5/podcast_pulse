FROM python:3.9

# ffmpeg needed for services
RUN apt-get update && apt-get install -y software-properties-common
RUN apt-get install -y ffmpeg

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt && rm -rf /root/.cache/pip

#
COPY ./app /code/app
COPY ./.env /code/.env

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]