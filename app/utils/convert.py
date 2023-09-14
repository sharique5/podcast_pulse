import os
from pydub import AudioSegment


def convert_mp4_to_wav_pydub(mp4_file_path):
  audio = AudioSegment.from_file(mp4_file_path, format="mp4")
  base, ext = os.path.splitext(mp4_file_path)
  wav_file = base + '.wav'
  audio.export(wav_file, format="wav")
  return wav_file