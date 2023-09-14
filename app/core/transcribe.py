import os
import azure.cognitiveservices.speech as speechsdk

def speech_continuous_recognition(audio_file_path):
    transcript_chunks = []
    done = False
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv("SPEECH_KEY"), region=os.getenv("SPEECH_REGION"))
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=False, filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                               audio_config=audio_config)
    
    def stop_cb(evt):
        done = True
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()

    def append_transcript(evt):
        print('{}'.format(evt.result.text))
        transcript_chunks.append(evt.result.text)

    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    speech_recognizer.recognized.connect(append_transcript)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)


    speech_recognizer.start_continuous_recognition()
    if done is True:
        return " ".join(transcript_chunks)
        