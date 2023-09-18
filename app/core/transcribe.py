import os
import time
import asyncio
import azure.cognitiveservices.speech as speechsdk
from app.utils.redis_consts import set_transcription_status, is_transcription_running

async def speech_continuous_recognition_old(file_id):
    curr_dir = os.path.dirname(os.path.abspath(__file__)) 
    audio_file = os.path.normpath(os.path.join(curr_dir, "../", "../", "audio", f"{file_id}.wav"))
    transcript_file = os.path.normpath(os.path.join(curr_dir, "../", "../", "transcripts", f"{file_id}.txt"))
    print("These are files {} and {}".format(audio_file, transcript_file))
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv("SPEECH_KEY"), region=os.getenv("SPEECH_REGION"))
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=False, filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                               audio_config=audio_config)
    
    set_transcription_status(False)
    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        set_transcription_status(True)
        speech_recognizer.stop_continuous_recognition()
        return

    def write_transcript(evt):
        print("Chunk came here....")
        with open(transcript_file, "a") as tfile:
             tfile.write(evt.result.text + "\n")

    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    speech_recognizer.recognized.connect(write_transcript)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)


    speech_recognizer.start_continuous_recognition()
    while is_transcription_running():
        time.sleep(.5) 



async def speech_continuous_recognition(file_id):
    curr_dir = os.path.dirname(os.path.abspath(__file__)) 
    audio_file = os.path.normpath(os.path.join(curr_dir, "../", "../", "audio", f"{file_id}.wav"))
    transcript_file = os.path.normpath(os.path.join(curr_dir, "../", "../", "transcript", f"{file_id}.txt"))
    print("These are files {} and {}".format(audio_file, transcript_file))
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv("SPEECH_KEY"), region=os.getenv("SPEECH_REGION"))
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=False, filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                               audio_config=audio_config)
    
    def on_recognized(event_args):
        print("Recognized: {}".format(event_args.result.text))
    
    def on_no_match(event_args):
        print("No speech could be recognized")

    def on_canceled(event_args):
        cancellation_details = event_args.result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.reason_details))


    speech_recognizer.recognized.connect(on_recognized)
    speech_recognizer.recognizing.connect(on_no_match)
    speech_recognizer.canceled.connect(on_canceled)

    await speech_recognizer.start_continuous_recognition()


def runner(file_id):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(speech_continuous_recognition(file_id))
    except KeyboardInterrupt:
        pass