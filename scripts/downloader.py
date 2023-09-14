import argparse
from pytube import YouTube
import os

parser = argparse.ArgumentParser(description='Generating audio file from YouTube URL')
parser.add_argument('-u', "--Url", required = True, help="YouTube URL")
parser.add_argument('-d', "--Destination", help="Save file at given path")
parser.add_argument('-f', "--Format", required = True, help="Format of the audio output file")
args = parser.parse_args()

yt_url = YouTube(args.Url)
audio_list = list(filter(lambda x: x['mimeType'].startswith('audio') == True, yt_url.streaming_data['adaptiveFormats']))

try:
    default_english_audio_flag = 0
    unique_itags = set()
    for i in audio_list:
        unique_itags.add(i['itag'])
        if not i['audioTrack']['displayName'].startswith('English'):
            default_english_audio_flag += 1
    default_english_audio_flag = (int)(default_english_audio_flag/len(unique_itags))
    audio = yt_url.streams.filter(only_audio=True)[default_english_audio_flag]
except KeyError:
    audio = yt_url.streams.filter(only_audio=True).first()
    

destination = args.Destination
out_file = audio.download(output_path=destination)
base, ext = os.path.splitext(out_file)

audio_format = args.Format
new_file = base + audio_format
os.rename(out_file, new_file)