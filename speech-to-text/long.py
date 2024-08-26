import os
from google.cloud import speech_v1p1beta1 as speech
import time
# Set up your Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cred.json"

def transcribe_long_audio(audio_uri):
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=audio_uri)
    config = speech.RecognitionConfig(
        # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        language_code="en-IN",
    )
    print(config)
    operation = client.long_running_recognize(config=config, audio=audio)
    while not operation.done():
        print("Still processing...")
        time.sleep(10)  # Sleep for 10 seconds before checking again

    # response = operation.result(timeout=900)

    print("Waiting for operation to complete...")
    try:
        response = operation.result(timeout=900)
    except Exception as e:
        print(f"Error during speech recognition: {e}")

    # response = operation.result(timeout=600)  # Adjust timeout as needed
    print(response)
    # Print the transcription results
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

if __name__ == "__main__":
    # Replace with your Cloud Storage URI for the audio file
    audio_uri = "gs://my-audio-bucket-prashant/1. How to optimally learn from case-studies in the course.mp3"
    # audio_uri = "gs://my-audio-bucket-prashant/speech.wav"
    # audio_uri = "gs://my-audio-bucket-prashant/audio.wav"
    transcribe_long_audio(audio_uri)
