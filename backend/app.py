from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from faster_whisper import WhisperModel
import uuid,json
from emotion_analysis import predict_emotion_from_audio
from voice_features import extract_voice_features
from llm_evaluator import evaluate_full_response
from llm_evaluator import overall_report
from llm_evaluator import generate_questions

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model once
model_size = "tiny"  # or "base" for slightly better accuracy
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
    # if "audio" not in request.files.getlist:
    #     return jsonify({"error": "No audio file found"}), 400

    files = request.files.getlist("audio")
    question_json = request.form.get("questions")
    questions = json.loads(question_json)
    final_res=[]
    for i in range(len(files)):
        # filename = f"{uuid.uuid4()}.wav"
        filename = f"audio_{i}.wav"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        files[i].save(filepath)

        try:
            # result = model.transcribe(filepath)
            # transcript = result["text"]
            transcript = transcribe_audio(filepath)
            question = questions[i] if i < len(questions) else None
            # Detect emotion
            # emotion = predict_emotion_from_audio(filepath)
            features = extract_voice_features(filepath)
            result = evaluate_full_response(
                question=question,
                transcript=transcript,
                emotion="neu",
                features=features
            )
            x = {"transcript": transcript,"emotion": "neu","features":features,"result":result}
            # print(x)
            # return jsonify({"transcript": transcript,"emotion": emotion,"features":features,"result":result})
            final_res.append({"transcript": transcript,"emotion": "neu","features":features,"result":result})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"result":final_res})

@app.route("/report",methods=["POST"])
def generate_report():
    try:
        data = request.get_json()
        qa_analysis = data.get("analysis")

        if not qa_analysis or not isinstance(qa_analysis, list):
            return jsonify({"error": "Missing or invalid 'analysis' array"}), 400
        
        report = overall_report(qa_analysis)
        return jsonify({"report": report})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_questions", methods=["POST"])
def generate_custom_questions():
    data = request.json
    company = data.get("company")
    role = data.get("role")
    interview_type = data.get("interview_type")
    job_description = data.get("job_description")
    years = data.get("years_experience")

    questions = generate_questions(company, role, interview_type, job_description,years)
    return jsonify({"initial_questions": questions})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
