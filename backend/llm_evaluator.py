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
  "score": <0–10>,                # Overall score based on content
  "confidence_score": <0–10>,     # How confidently they sounded
  "feedback": "<1–2 sentence summary of their performance>",
  "improvement": "<2-3 suggestions to improve>"
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
