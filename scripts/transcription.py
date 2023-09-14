# import azure.cognitiveservices.speech as speechsdk
import config

# # Creates an instance of a speech config with specified subscription key and service region.
# # Replace with your own subscription key and region.
# speech_key, service_region = config.Key1, config.Region
# speech_config=speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# # Creates an audio configuration that points to an audio file.
# # Replace with your own audio filename.
# audio_filename = "Steve Jobs Secrets of Life.wav"
# audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)

# # Creates a recognizer with the given settings
# speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

# print("Recognizing first result...")

# # Starts speech recognition, and returns after a single utterance is recognized. The end of a
# # single utterance is determined by listening for silence at the end or until a maximum of 15
# # seconds of audio is processed.  The task returns the recognition text as result. 
# # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# # shot recognition like command or query. 
# # For long-running multi-utterance recognition, use start_continuous_recognition() instead.

# result = speech_recognizer.recognize_once()

# # Checks result.
# if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#     print("Recognized by Azure: {}".format(result.text))
# elif result.reason == speechsdk.ResultReason.NoMatch:
#     print("No speech could be recognized: {}".format(result.no_match_details))
# elif result.reason == speechsdk.ResultReason.Canceled:
#     cancellation_details = result.cancellation_details
#     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#     if cancellation_details.reason == speechsdk.CancellationReason.Error:
#         print("Error details: {}".format(cancellation_details.error_details))


# ------------- END ----------------

import os
import sys
import time
import azure.cognitiveservices.speech as speechsdk

subscription_key = config.Key1
region = config.Region

# Create a callback to terminate the transcription once the full audio
# has been transcribed.

done = False
def stop_cb(evt):
    """Callback to stop continuous recognition upon receiving an event `evt`"""
    speech_recognizer.stop_continuous_recognition()
    global done
    done = True

# Create an instance of a speech config with the provided subscription
# key and service region. Then create an audio configuration to load
# the audio from file rather than from microphone. A sample audio file
# is available as harvard.wav from:
#
# https://github.com/realpython/python-speech-recognition/raw/master/
# audio_files/harvard.wav
#
# A recognizer is then created with the given settings.

pth = "(Life) Advice From The Creator of C++.wav"

speech_config     = speechsdk.SpeechConfig(subscription=subscription_key,
                                           region=region)
audio_config      = speechsdk.audio.AudioConfig(use_default_microphone=False,
                                                filename=pth)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                               audio_config=audio_config)

# We connect callbacks to the events fired by the speech
# recognizer. Most are commented out as examples here to allow tracing
# if you are interested in exploring the interactions with the server.
#
# speech_recognizer.recognizing.connect(lambda evt:
#                                       print('RECOGNIZING: {}'.format(evt)))
# speech_recognizer.session_started.connect(lambda evt:
#                                           print('STARTED: {}'.format(evt)))
# speech_recognizer.session_stopped.connect(lambda evt:
#                                           print('STOPPED {}'.format(evt)))
# speech_recognizer.canceled.connect(lambda evt:
#                                    print('CANCELED {}'.format(evt)))

# This callback provides the actual transcription.

speech_recognizer.recognized.connect(lambda evt:
                                     print('{}'.format(evt.result.text)))

# Stop continuous recognition on either session stopped or canceled
# events.

speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

# Start continuous speech recognition, and then perform
# recognition. For long-running recognition we use
# start_continuous_recognition().

speech_recognizer.start_continuous_recognition()
while not done:
    time.sleep(.5)