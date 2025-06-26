from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from faster_whisper import WhisperModel
import uuid
from emotion_analysis import predict_emotion_from_audio
from voice_features import extract_voice_features
from llm_evaluator import evaluate_full_response

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model once
model_size = "base"  # or "base" for slightly better accuracy
model = WhisperModel(model_size, device="cpu", compute_type="int8")  # use int8 for speed

def transcribe_audio(file_path):
    try:
        segments, info = model.transcribe(file_path)

        full_text = ""
        for segment in segments:
            full_text += segment.text.strip() + " "

        return full_text.strip()

    except Exception as e:
        return f"Transcription failed: {str(e)}"

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file found"}), 400

    audio_file = request.files["audio"]
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    audio_file.save(filepath)

    try:
        # result = model.transcribe(filepath)
        # transcript = result["text"]
        transcript = transcribe_audio(filepath)
        question = "Tell me about yourself"
        # Detect emotion
        emotion = predict_emotion_from_audio(filepath)
        features = extract_voice_features(filepath)
        result = evaluate_full_response(
            question=question,
            transcript=transcript,
            emotion=emotion,
            features=features
        )
        return jsonify({"transcript": transcript,"emotion": emotion,"features":features,"result":result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)
