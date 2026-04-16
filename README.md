# JARVIS AI - Biometric Desktop Assistant 🛡️🤖

An advanced AI-powered desktop assistant with face recognition security, system automation, and natural language processing.

### ✨ Features:
- **Biometric Security:** Unlocks only for Shivam Sir using LBPH Face Recognition.
- **Smart GUI:** Multi-threaded PyQt6 dashboard with real-time HUD (Time/Date/Status).
- **Dual-Brain Logic:** Uses Google Gemini 2.0 API for AI and local APIs for Weather/News.
- **Automation:** WhatsApp messaging, App launching (Telegram, Chrome, etc.), and System monitoring.

### 🛠️ Tech Stack:
- **Language:** Python 3.13
- **AI/CV:** OpenCV, LBPH Algorithm, Google Gemini API
- **GUI:** PyQt6
- **Automation:** PyWhatKit, PyAutoGUI, SpeechRecognition

### 🚀 Setup:
1. `pip install -r requirements.txt`
2. Run `face_data.py` to capture samples.
3. Run `face_train.py` to train the model.
4. Launch `python Main_GUI.py`.