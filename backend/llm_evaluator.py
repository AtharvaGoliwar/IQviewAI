import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def evaluate_full_response(question, transcript, emotion, features):
    prompt = f"""
You are an AI **interviewer** and **evaluator** for mock interviews. Your role is to assess how well a candidate answered a question during a job interview.

You will receive:
1. The interview question
2. The candidate’s answer (transcribed from their speech)
3. Detected **emotion** during the answer
4. Detailed **voice features** that reflect how confidently they spoke (pitch, loudness, tempo, pauses)

---

### Evaluate the candidate on two axes:
- **Content Quality**: Was their answer relevant, clear, and well-structured?
- **Spoken Confidence**: Based on pitch, loudness, tempo, and pauses, how confidently did they speak?

---

### INPUT:

**Interview Question:**
{question}

**Candidate's Answer (transcribed):**
{transcript}

**Detected Emotion:**
{emotion}

**Voice Features:**
- Average Pitch: {features.get("avg_pitch")} Hz
- Pitch Variability (StdDev): {features.get("pitch_stddev")}
- Average Energy: {features.get("avg_energy")}
- Energy Variability: {features.get("energy_stddev")}
- Tempo: {features.get("tempo")} BPM
- Pause Ratio: {features.get("pause_ratio")}
- Speech Duration: {features.get("speech_duration_sec")} sec
- Total Duration: {features.get("total_duration_sec")} sec
- Speaking Rate: {features.get("speaking_rate")}

---

### Based on the above, give an **interview evaluation** in the following JSON format:

{{
  "score": <0–100>,                # Overall score based on content
  "confidence_score": <0–10>,     # How confidently they sounded
  "feedback": "<1–2 sentence summary of their performance as string>",
  "improvement": "<2-3 suggestions to improve and store the suggestions in an array>"
}}

Be fair but honest — and sound like a helpful interview coach.
"""


    try:
        response = model.generate_content(prompt)
        raw = response.text

        # Try parsing JSON from Gemini response
        import json, re
        json_str = re.search(r'\{[\s\S]*?\}', raw)
        if json_str:
            return json.loads(json_str.group())
        else:
            return {
                "score": 0,
                "confidence_score": 0,
                "feedback": "Could not parse Gemini output.",
                "improvement": "Try again.",
                "raw": raw
            }
    except Exception as e:
        return {
            "score": 0,
            "confidence_score": 0,
            "feedback": "Evaluation failed.",
            "improvement": "Please retry.",
            "error": str(e)
        }


def overall_report(question_responses):
    prompt = f"""
You are an AI interview coach.

Below is a list of question-answer evaluations from a mock interview. Each item contains:
- the interview question,
- the candidate's answer transcript,
- a score out of 10 for content quality,
- a confidence score out of 10 (based on voice tone and delivery),
- the detected emotion during the response,
- and specific improvement feedback.

Your task is to:
1. Evaluate the overall performance across all answers.
2. Identify common strengths and weaknesses in content and tone.
3. Provide an overall confidence and communication score out of 10.
4. Provide a total interview performance score out of 10.
5. Give a 2–3 sentence summary of the candidate’s performance in a string.
6. Give 3 actionable suggestions to improve for future interviews and store the result in an array.

Here is the data:
{question_responses}

Respond in the following format:

{{
  "overall_score": <0-100> ,
  "confidence_score": <0-10> ,
  "summary": "...",
  "advice": ["...", "...", "..."]
  "number_of_questions":{len(question_responses)}
}}
"""
    try:
        response = model.generate_content(prompt)
        raw = response.text

        # Try parsing JSON from Gemini response
        import json, re
        json_str = re.search(r'\{[\s\S]*?\}', raw)
        if json_str:
            return json.loads(json_str.group())
        else:
            return {
                "overall_score": 0,
                "confidence_score": 0,
                "summary": "Could not parse Gemini output.",
                "advice": [],
                "raw": raw
            }
    except Exception as e:
        return {
            "overall_score": 0,
            "confidence_score": 0,
            "summary": "Could not parse Gemini output.",
            "advice": [],
            "error": str(e)
        }

