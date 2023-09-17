import os
import traceback
import shortuuid
from pytube import YouTube
from utils import convert

async def download_youtube_podcast(yt_url):
  try:
    yt = YouTube(yt_url)
    audio_list = list(filter(lambda x: x['mimeType'].startswith('audio') == True, yt.streaming_data['adaptiveFormats']))
    default_english_audio_position = 0
    unique_itags = set()
    for audio in audio_list:
      unique_itags.add(audio['itag'])
      language_display_name = audio.get('audioTrack', {}).get('displayName', None)
      if language_display_name is not None and not language_display_name.startswith("English"):
        default_english_audio_position += 1
        
    english_audio_position = default_english_audio_position
    audio = yt.streams.filter()[english_audio_position]
    curr_dir = os.path.dirname(os.path.abspath(__file__)) 
    file_path = os.path.normpath(os.path.join(curr_dir, "../", "../", "audio"))
    file_name = shortuuid.uuid()
    downloaded_file = audio.download(output_path=file_path, filename=file_name)    
    wav_file = convert.convert_mp4_to_wav_pydub(downloaded_file)
    os.remove(downloaded_file)
    return wav_file

  except Exception:
    print(traceback.format_exc())
    return None