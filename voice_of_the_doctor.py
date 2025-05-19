# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

# Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS
from pydub import AudioSegment

def text_to_speech_with_gtts(input_text, output_filepath):
    try:
        language = "en"
        audioobj = gTTS(
            text=input_text,
            lang=language,
            slow=False
        )
        audioobj.save(output_filepath)
    except Exception as e:
        print(f"Error during gTTS generation: {e}")
        return "Sorry, I could not generate the audio."


