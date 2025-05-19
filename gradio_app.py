import os
import gradio as gr
from dotenv import load_dotenv
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from brain_of_the_doctor import encoded_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "chatgpt_app")
USERS_COLLECTION = os.getenv("USERS_COLLECTION", "users")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db[USERS_COLLECTION]

system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purpose. 
What's in this image? Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Do not say 'In the image I see' but say 'With what I see, I think you have ....'
Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""

def register(username, password):
    username = username.strip()
    password = password.strip()
    if not username or not password:
        return "Username and password cannot be empty."

    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        return "Username already exists! Please choose a different username."

    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        "username": username,
        "password": hashed_password
    })

    return "Registration successful! You can now log in."

def login(username, password):
    username = username.strip()
    password = password.strip()
    user = users_collection.find_one({"username": username})
    if user and check_password_hash(user['password'], password):
        return "Login successful!"
    else:
        return "Invalid username or password!"

def process_inputs(audio_filepath, image_filepath):
    if not audio_filepath or not os.path.exists(audio_filepath) or os.path.getsize(audio_filepath) == 0:
        speech_to_text_output = "Sorry, I could not capture your voice. Please try again."
    else:
        try:
            speech_to_text_output = transcribe_with_groq(
                GROQ_API_KEY=os.getenv("GROQ_API_KEY"),
                audio_filepath=audio_filepath,
                stt_model="whisper-large-v3"
            )
        except Exception:
            speech_to_text_output = "Sorry, I could not transcribe the audio."

    doctor_response = "No image provided for me to analyze."
    if image_filepath:
        try:
            encoded = encoded_image(image_filepath)

            if not encoded:
                doctor_response = "Sorry, I could not encode the image."
            else:
                doctor_response = analyze_image_with_query(
                    query=system_prompt + speech_to_text_output,
                    encoded_image=encoded,
                    model="meta-llama/llama-4-scout-17b-16e-instruct"
                )
        except Exception:
            doctor_response = "Sorry, I could not analyze the image."

    try:
        text_to_speech_with_gtts(input_text=doctor_response, output_filepath="final.mp3")
        audio_outpath = "final.mp3"
    except Exception:
        audio_outpath = None

    return speech_to_text_output, doctor_response, audio_outpath

def auth_interface(username, password, action):
    if action == "Register":
        return register(username, password)
    elif action == "Login":
        return login(username, password)
    return "Invalid action!"

with gr.Blocks(css="""
    body {background-color: #f4f7f6;}
    .auth-section {
        background-color: #eef6f8;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        max-width: 420px;
        margin: auto;
        margin-top: 40px;
    }
    .app-section {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.12);
        max-width: 900px;
        margin: 40px auto;
    }
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #1b4965;
        margin-bottom: 20px;
        text-align: center;
    }
    .input-label {
        color: #0b3c5d;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .button-primary {
        background-color: #1b4965 !important;
        color: white !important;
        font-size: 17px !important;
        border-radius: 8px !important;
        padding: 12px 0 !important;
        margin-top: 15px !important;
        width: 100% !important;
    }
    .button-primary:hover {
        background-color: #144055 !important;
    }
    .auth-radio {
        margin-top: 10px;
        margin-bottom: 15px;
        font-weight: 600;
        color: #0b3c5d;
    }
""") as app:

    login_state = gr.State(value={"logged_in": False, "username": ""})

    with gr.Column(elem_classes="auth-section", visible=True) as auth_interface_row:
        gr.Markdown("<div class='section-title'>Welcome to MediSense</div>", elem_id="welcome-title")
        username = gr.Textbox(label="Username", interactive=True, elem_classes="input-label")
        password = gr.Textbox(label="Password", type="password", interactive=True, elem_classes="input-label")
        action = gr.Radio(choices=["Login", "Register"], label="Select Action", interactive=True, elem_classes="auth-radio")
        submit_btn = gr.Button("Submit", elem_classes="button-primary")
        auth_output = gr.Textbox(label="Authentication Output", interactive=False)

    with gr.Column(elem_classes="app-section", visible=False) as main_interface_row:
        gr.Markdown("<div class='section-title'>MediSense AI - Healthcare Assistant</div>")
        with gr.Row():
            with gr.Column():
                audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record your voice (mp3)", format="mp3")
                image_input = gr.Image(type="filepath", label="Upload Medical Image")
                process_btn = gr.Button("Analyze", elem_classes="button-primary")
            with gr.Column():
                speech_output = gr.Textbox(label="Transcribed Speech", lines=6)
                doctor_response_output = gr.Textbox(label="Doctor AI Response", lines=8)
                audio_output = gr.Audio(label="Audio Response")
        logout_btn = gr.Button("Logout", elem_classes="button-primary", variant="secondary")

    def handle_auth(username_val, password_val, action_val, state):
        result = auth_interface(username_val, password_val, action_val)
        if result == "Login successful!":
            state["logged_in"] = True
            state["username"] = username_val.strip()
            return result, gr.update(visible=False), gr.update(visible=True), state
        elif result == "Registration successful! You can now log in.":
            return result, gr.update(visible=True), gr.update(visible=False), state
        else:
            return result, gr.update(visible=True), gr.update(visible=False), state

    submit_btn.click(handle_auth,
                     inputs=[username, password, action, login_state],
                     outputs=[auth_output, auth_interface_row, main_interface_row, login_state])

    process_btn.click(process_inputs,
                      inputs=[audio_input, image_input],
                      outputs=[speech_output, doctor_response_output, audio_output])

    def handle_logout(state):
        state["logged_in"] = False
        state["username"] = ""
        return gr.update(value="Logged out successfully."), gr.update(visible=True), gr.update(visible=False), state

    logout_btn.click(handle_logout,
                     inputs=[login_state],
                     outputs=[auth_output, auth_interface_row, main_interface_row, login_state])

if __name__ == "__main__":
    app.launch(debug=True, server_name="127.0.0.1", server_port=7861)
