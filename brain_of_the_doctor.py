# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

# Step1: Setup GROQ API key
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Step2: Convert image to required format
import base64

def encoded_image(image_path):   
    try:
        image_file = open(image_path, "rb")
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

    return base64.b64encode(image_file.read()).decode('utf-8')

# Step3: Setup Multimodal LLM 
from groq import Groq

def analyze_image_with_query(query, model, encoded_image):
    try:
        client = Groq()  
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        return "Sorry, I could not analyze the image."

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }
    ]
    
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    except Exception as e:
        print(f"Error during API call: {e}")
        return "Sorry, I could not analyze the image."

    return chat_completion.choices[0].message.content
