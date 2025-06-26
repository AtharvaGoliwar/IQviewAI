import React, { useRef, useState } from "react";
import "./VoiceRecorder.css";

export default function VoiceRecorder() {
  const mediaRecorderRef = useRef(null);
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const chunks = [];

    mediaRecorder.ondataavailable = (e) => {
      chunks.push(e.data);
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: "audio/wav" });
      setAudioURL(URL.createObjectURL(blob));
      uploadAudio(blob);
    };

    mediaRecorder.start();
    mediaRecorderRef.current = mediaRecorder;
    setIsRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  const uploadAudio = async (blob) => {
    const formData = new FormData();
    formData.append("audio", blob, "recording.wav");

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      alert(data.transcript);
    } catch (err) {
      console.error("Upload failed", err);
    }
  };

  return (
    <div className="recorder-container">
      <h2 className="recorder-title">🎤 AI Interview Voice Recorder</h2>
      <button
        onClick={isRecording ? stopRecording : startRecording}
        className="record-btn"
      >
        {isRecording ? "Stop Recording" : "Start Recording"}
      </button>

      {audioURL && (
        <div className="audio-box">
          <audio controls src={audioURL} />
        </div>
      )}
    </div>
  );
}
