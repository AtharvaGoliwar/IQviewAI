# 🎤 IQviewAI – AI-Powered Mock Interview Analyzer

**IQviewAI** is a smart voice-based mock interview platform that simulates real interview sessions using AI. It dynamically generates custom interview questions based on role, company, and job description, records your spoken responses, and analyzes your performance using advanced LLMs and speech processing.

---

## 🚀 Features

- 🎯 **Custom Question Generation**  
  Generates interview questions tailored to:
  - Role
  - Company
  - Interview type (technical, behavioral, etc.)
  - Job Description

- 🗣️ **Voice Input and AI Question Playback**  
  - Users answer questions via microphone
  - AI voice reads each question aloud

- 🧠 **Emotion & Confidence Analysis**  
  - Detects emotion, pitch, energy, and prosodic features from speech
  - Evaluates how confidently you spoke

- 📄 **LLM-Based Content Feedback**  
  - Scores the content of each answer
  - Gives adaptive follow-up questions
  - Provides detailed feedback after the session

- 📊 **Interview Report Generation**  
  - Final summary with:
    - Confidence rating
    - Feedback
    - Improvement tips
    - Overall score

---

## 🛠️ Tech Stack

### Frontend:
- React.js + Vite
- Tailwind CSS
- Web Speech API (Text-to-Speech)

### Backend:
- Flask
- Gemini 2.5 Flash (Google Generative AI)
- Faster-Whisper (Speech-to-Text)
- Transformers (HuggingFace)
- Librosa (Audio feature extraction)
- Torch + torchaudio

---

## 🧪 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/AtharvaGoliwar/IQviewAI.git
cd IQviewAI
````

---

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On Mac/Linux

pip install -r requirements.txt
```

Create a `.env` file and add:

```
GEMINI_API_KEY=your_api_key_here
```

Run server:

```bash
python app.py
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Usage

1. Enter your **role**, **company**, **interview type**, and **job description**
2. Click **Start Interview**
3. Listen to the AI question → Record your answer
4. After each answer, AI may ask follow-up questions
5. Press **End Interview** any time
6. View your personalized interview **report**

---

## 📁 Folder Structure

```
IQviewAI/
├── backend/
│   ├── app.py
│   ├── emotion_analysis.py
│   ├── llm_evaluator.py
│   ├── voice_features.py
│   └── requirements.txt
├── frontend/
│   └── [React]
└── README.md
```

---

## 📌 Future Enhancements

* 🔐 User authentication + saved session history
* 🧩 Integration with real job listings from LinkedIn/Indeed
* 📹 Video-based confidence & gesture detection
* 🌐 Deployment with Docker on Render/Vercel

---

## 🧑‍💻 Built by

Atharva Goliwar
Feel free to contribute via pull requests!

---
