from dotenv import load_dotenv
load_dotenv()

#step1: setup audio recorder(ffmpeg & portaudio)
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
logging.basicConfig(level=logging.INFO,format='%(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_lfimit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

audio_filepath="patient_voice_test_for_patient.mp3"
#record_audio(file_path=audio_filepath)  #it will save the recorded audio in mp3 format in patient_voice_test_for_patient.mp3 file  

#Step2: Setup Speech to text–STT–model for transcription
import os
from groq import Groq 

#GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Error: GROQ_API_KEY is missing. Set it in the environment variables.")


stt_model="whisper-large-v3"

def transcribe_with_groq(GROQ_API_KEY, audio_filepath, stt_model="whisper-large-v3"):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Please set it in the environment variables.")
    
    client=Groq(api_key=GROQ_API_KEY)
    
      # Open the audio file properly using `with`
    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )


    # Return the transcribed text instead of just printing
    return transcription.text

# Example Usage
audio_file_path = "sample_audio.mp3"

if os.path.exists(audio_file_path):
    try:
        result = transcribe_with_groq(GROQ_API_KEY, audio_file_path)
        print("Transcription:", result)
    except Exception as e:
        print("Error:", e)
else:
    print(f"Error: The file {audio_file_path} does not exist. Please record an audio file first.")




