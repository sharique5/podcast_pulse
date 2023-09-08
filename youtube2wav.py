import os
import certifi
import ssl
from pytube import YouTube
import moviepy.editor as mp
import psutil
import re

ssl._create_default_https_context = ssl._create_unverified_context
YouTube.DEFAULT_RETRIES = 5
YouTube.DEFAULT_CA_CERTS_PATH = certifi.where()


def clean_filename(filename):
    cleaned_filename = re.sub(r'[\\/:*?"<>|@!#$%^&*]', '_', filename)
    return cleaned_filename


def download_and_convert(url):
    try:
        yt = YouTube(url)
        video_title = yt.title
        cleaned_title = clean_filename(video_title)
        video_stream = yt.streams.filter(file_extension="mp4", res="360p").first()
        mp4_file = f"{cleaned_title}"
        video_stream.download(filename=cleaned_title)
        wav_file = f"{cleaned_title}.wav"
        video_clip = mp.VideoFileClip(mp4_file)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(wav_file, codec='pcm_s16le', fps=44100)
        close_ffmpeg_processes()
        os.remove(mp4_file)
        print(f"Download and conversion completed: {wav_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def close_ffmpeg_processes():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if "ffmpeg" in process.info['name']:
                os.kill(process.info['pid'], psutil.signal.SIGTERM)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


if __name__ == "__main__":
    while True:
        youtube_url = input("Enter the YouTube URL (Type 'exit' to quit): ")
        if youtube_url.lower() == 'exit':
            break
        download_and_convert(youtube_url)