# from transformers import Wav2Vec2FeatureExtractor, HubertForSequenceClassification
# import torch
# import torchaudio

# # Load model and processor
# model_name = "superb/hubert-large-superb-er"
# processor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
# model = HubertForSequenceClassification.from_pretrained(model_name)
# model.eval()

# labels = model.config.id2label

# def predict_emotion_from_audio(file_path):
#     try:
#         # Load audio
#         speech, sr = torchaudio.load(file_path)

#         # Resample to 16kHz
#         if sr != 16000:
#             resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
#             speech = resampler(speech)

#         # Process and predict
#         inputs = processor(speech[0], sampling_rate=16000, return_tensors="pt")
#         with torch.no_grad():
#             logits = model(**inputs).logits
#             probs = torch.nn.functional.softmax(logits, dim=-1)

#         # Get predicted emotion and confidence
#         predicted_id = int(torch.argmax(probs))
#         emotion = labels[predicted_id]
#         confidence = float(probs[0][predicted_id])  # as a float, not tensor

#         # Fallback if confidence is very low
#         if confidence < 0.4:
#             return {
#                 "emotion": "uncertain",
#                 "confidence": round(confidence, 2)
#             }

#         return {
#             "emotion": emotion,
#             "confidence": round(confidence, 2)
#         }

#     except Exception as e:
#         return {
#             "emotion": "error",
#             "confidence": 0.0,
#             "error": str(e)
#         }


from transformers import Wav2Vec2FeatureExtractor, HubertForSequenceClassification
import torchaudio
import torch
import subprocess
import os

# Load model and feature extractor
model_name = "superb/hubert-large-superb-er"
processor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
model = HubertForSequenceClassification.from_pretrained(model_name)
model.eval()

labels = model.config.id2label
MODEL_ACCURACY = 0.84  # Approx accuracy on IEMOCAP or SUPERB-ER

def convert_to_wav(input_path):
    """Converts any audio to 16kHz mono WAV using ffmpeg."""
    output_path = input_path.replace(".wav", "_converted.wav")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-ar", "16000", "-ac", "1", output_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except subprocess.CalledProcessError:
        return None

def predict_emotion_from_audio(file_path):
    try:
        # Convert audio to compatible WAV format
        converted_path = convert_to_wav(file_path)
        if not converted_path or not os.path.exists(converted_path):
            return {
                "emotion": "error",
                "confidence": 0.0,
                "error": "Audio format conversion failed"
            }

        # Load and process audio
        speech, sr = torchaudio.load(converted_path)

        # Model expects 16kHz mono
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
            speech = resampler(speech)

        # Run inference
        inputs = processor(speech[0], sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.nn.functional.softmax(logits, dim=-1)

        predicted_id = int(torch.argmax(probs))
        emotion = labels[predicted_id]
        confidence = float(probs[0][predicted_id])

        # Clean up temp file
        os.remove(converted_path)

        # Return result with fallback if confidence is low
        if confidence < 0.4:
            return {
                "emotion": "uncertain",
                "confidence": round(confidence, 2),
                "model_accuracy": MODEL_ACCURACY
            }

        return {
            "emotion": emotion,
            # "confidence": round(confidence, 2),
            # "model_accuracy": MODEL_ACCURACY
        }

    except Exception as e:
        return {
            "emotion": "error",
            "confidence": 0.0,
            "error": str(e)
        }
