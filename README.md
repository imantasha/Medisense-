# 🩺 MediSense – AI Medical Chatbot

**MediSense** is an AI-powered medical chatbot designed to assist users in understanding and communicating their medical concerns using both **speech** and **image** inputs. It leverages **Whisper (Groq)** for speech-to-text, **Google TTS** for voice responses, and **MongoDB** to securely store user interactions. The frontend is built using **Gradio** for a seamless and interactive experience.

---

## 🚀 Features

- 🎤 **Speech-to-Text**: Convert voice input into text using Whisper API
- 🖼️ **Image Upload**: Accepts medical images for diagnosis assistance
- 💬 **AI-Powered Chat**: Delivers intelligent, doctor-like responses
- 🔊 **Text-to-Speech**: Replies are converted to audio using Google TTS
- 🗃️ **MongoDB** Integration: Stores user data and chat history
- 🖥️ **Gradio UI**: Clean and easy-to-use interface

---

##  Tech Stack

| Component          | Technology Used             |
|-------------------|-----------------------------|
| Backend            | Python                      |
| Frontend           | Gradio                      |
| Voice Input        | Whisper via Groq API        |
| Audio Output       | Google Text-to-Speech       |
| Database           | MongoDB                     |
| Data Handling      | Pandas, NumPy               |
| Visualization (Optional) | Matplotlib, Seaborn       |

---

## Installation & Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/imantasha/medisense-ai-chatbot.git
cd medisense-ai-chatbot

2. Create Virtual Environment & Install Dependencies
bash
Copy
Edit
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

3. Start the Application
bash
Copy
Edit
python gradio_app.py
📁 Project Structure
bash
Copy
Edit
medisense-ai-chatbot/
│
├── gradio_app.py               # Main UI logic using Gradio
├── voice_of_the_patient.py     # Handles voice input and transcription
├── db_utils.py                 # MongoDB operations
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
Future Enhancements
Google OAuth login

Role-Based Access Control (RBAC) for admin, doctor, and patient roles

Image-based disease classification using ML

Doctor-prescribed treatment suggestions

PDF prescription export




