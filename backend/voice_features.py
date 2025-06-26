import librosa
import numpy as np

def extract_voice_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=16000)

        # 1. Pitch
        pitch = librosa.yin(y, fmin=50, fmax=300)
        avg_pitch = float(np.mean(pitch))
        pitch_stddev = float(np.std(pitch))

        # 2. Energy (RMS)
        rms = librosa.feature.rms(y=y)[0]
        avg_energy = float(np.mean(rms))
        energy_stddev = float(np.std(rms))

        # 3. Tempo
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(tempo)

        # 4. Silence-based speech/pause analysis
        intervals = librosa.effects.split(y, top_db=30)
        speech_duration = sum((end - start) for start, end in intervals) / sr
        total_duration = librosa.get_duration(y=y, sr=sr)

        pause_ratio = 1 - (speech_duration / total_duration)
        speaking_rate = speech_duration / total_duration

        return {
            "avg_pitch": round(avg_pitch, 2),
            "pitch_stddev": round(pitch_stddev, 2),
            "avg_energy": round(avg_energy, 5),
            "energy_stddev": round(energy_stddev, 5),
            "tempo": round(tempo, 2),
            "pause_ratio": round(pause_ratio, 3),
            "speech_duration_sec": round(speech_duration, 2),
            "total_duration_sec": round(total_duration, 2),
            "speaking_rate": round(speaking_rate, 3)
        }

    except Exception as e:
        return {
            "error": str(e)
        }
