import moviepy.editor as mp
import os
import psutil
from pydub import AudioSegment


def convert_mp4_to_wav_pydub(mp4_file_path):
  audio = AudioSegment.from_file(mp4_file_path, format="mp4")
  base, ext = os.path.splitext(mp4_file_path)
  wav_file = base + '.wav'
  audio.export(wav_file, format="wav")
  return wav_file

def convert_mp4_to_wav(mp4_file_path):
  video_clip = mp.VideoFileClip(mp4_file_path)
  audio_clip = video_clip.audio
  base, ext = os.path.splitext(mp4_file_path)
  wav_file = base + '.wav'
  audio_clip.write_audiofile(wav_file, codec='pcm_s16le', fps=44100)
  close_ffmpeg_processes()


def close_ffmpeg_processes():
  for process in psutil.process_iter(attrs=['pid', 'name']):
      try:
        if "ffmpeg" in process.info['name']:
          os.kill(process.info['pid'], psutil.signal.SIGTERM)
      except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
