import React, { useState, useRef, useEffect } from "react";
import {
  Play,
  Square,
  FileText,
  Briefcase,
  Clock,
  User,
  Mic,
  MicOff,
  CheckCircle,
  Star,
  TrendingUp,
} from "lucide-react";
import "./AIInterviewApp.css";

const AIInterviewApp = () => {
  const [currentView, setCurrentView] = useState("home");
  const [showDialog, setShowDialog] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [interviewData, setInterviewData] = useState({
    jobDescription: "",
    companyName: "",
    yearsExperience: "",
    interviewType: "technical",
  });

  const [questions, setQuestions] = useState([]);
  const [recordings, setRecordings] = useState([]);
  const [results, setResults] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // Sample questions based on interview type
  const sampleQuestions = {
    technical: [
      "Tell me about a challenging technical problem you've solved recently.",
      "How would you optimize a slow-performing database query?",
      "Explain the difference between REST and GraphQL APIs.",
      "How do you handle error handling in your applications?",
      "What's your approach to code testing and quality assurance?",
    ],
    hr: [
      "Tell me about yourself and your career journey.",
      "Why are you interested in this position?",
      "Describe a time when you had to work with a difficult team member.",
      "Where do you see yourself in 5 years?",
      "What motivates you in your work?",
    ],
  };

  // Sample results for demonstration
  const sampleResults = {
    answers: [
      {
        question:
          "Tell me about a challenging technical problem you've solved recently.",
        answer:
          "I worked on optimizing our API response times by implementing caching strategies...",
        confidence: 85,
        duration: "2:30",
      },
      {
        question: "How would you optimize a slow-performing database query?",
        answer:
          "I would start by analyzing the query execution plan and looking for missing indexes...",
        confidence: 78,
        duration: "1:45",
      },
      {
        question: "Explain the difference between REST and GraphQL APIs.",
        answer:
          "REST is a stateless architecture while GraphQL provides more flexible data fetching...",
        confidence: 92,
        duration: "2:15",
      },
    ],
    summary:
      "Strong technical knowledge with good communication skills. Showed confidence in database optimization and API design concepts.",
    overallScore: 85,
    improvements: [
      "Consider providing more specific examples when discussing past experiences",
      "Work on reducing filler words during explanations",
      "Practice explaining complex concepts more concisely",
    ],
  };

  const handleStartRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/wav",
        });
        setRecordings((prev) => [...prev, audioBlob]);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Please allow microphone access to record your answers.");
    }
  };

  const handleStopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleGenerateInterview = () => {
    if (
      !interviewData.jobDescription ||
      !interviewData.companyName ||
      !interviewData.yearsExperience
    ) {
      alert("Please fill in all required fields.");
      return;
    }

    setQuestions(sampleQuestions[interviewData.interviewType]);
    setCurrentQuestion(0);
    setShowDialog(false);
    setCurrentView("interview");
  };

  const handleNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion((prev) => prev + 1);
    }
  };

  const handleCompleteInterview = () => {
    // Simulate AI processing
    uploadAudio(recordings);
    setTimeout(() => {
      setResults(sampleResults);
      setCurrentView("results");
    }, 2000);
  };

  const uploadAudio = async (blob) => {
    const formData = new FormData();
    formData.append("audio", blob, "recording.wav");
    formData.append("questions", sampleQuestions.technical);

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

  const getConfidenceClass = (score) => {
    if (score >= 80) return "confidence-high";
    if (score >= 60) return "confidence-medium";
    return "confidence-low";
  };

  const getConfidenceLabel = (score) => {
    if (score >= 80) return "High";
    if (score >= 60) return "Medium";
    return "Low";
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1 className="header-title">AI Interview Assistant</h1>
          <p className="header-subtitle">
            Practice and improve your interview skills
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Home View */}
        {currentView === "home" && (
          <div className="home-view">
            <div className="hero-section">
              <div className="hero-icon">
                <Briefcase size={40} />
              </div>
              <h2 className="hero-title">Ready to Practice?</h2>
              <p className="hero-description">
                Start your AI-powered interview practice session. Get
                personalized feedback on your answers, confidence levels, and
                areas for improvement.
              </p>
              <button
                onClick={() => setShowDialog(true)}
                className="btn btn-primary btn-large"
              >
                <Play size={20} />
                Take Interview
              </button>
            </div>

            <div className="features-grid">
              <div className="feature-card">
                <FileText size={32} />
                <h3>Detailed Analysis</h3>
                <p>Get comprehensive feedback on each answer</p>
              </div>
              <div className="feature-card">
                <TrendingUp size={32} />
                <h3>Confidence Scoring</h3>
                <p>Track your confidence levels throughout</p>
              </div>
              <div className="feature-card">
                <Star size={32} />
                <h3>Improvement Tips</h3>
                <p>Personalized suggestions for growth</p>
              </div>
            </div>
          </div>
        )}

        {/* Interview View */}
        {currentView === "interview" && (
          <div className="interview-view">
            <div className="interview-header">
              <div>
                <h2 className="interview-title">Interview in Progress</h2>
                <p className="interview-progress">
                  Question {currentQuestion + 1} of {questions.length}
                </p>
              </div>
              <div className="interview-info">
                <p>Company: {interviewData.companyName}</p>
                <p>Type: {interviewData.interviewType}</p>
              </div>
            </div>

            <div className="question-section">
              <div className="question-card">
                <h3 className="question-text">{questions[currentQuestion]}</h3>
              </div>

              <div className="recording-controls">
                {!isRecording ? (
                  <button
                    onClick={handleStartRecording}
                    className="btn btn-record"
                  >
                    <Mic size={20} />
                    Start Recording
                  </button>
                ) : (
                  <button
                    onClick={handleStopRecording}
                    className="btn btn-stop"
                  >
                    <Square size={20} />
                    Stop Recording
                  </button>
                )}
              </div>

              {isRecording && (
                <div className="recording-indicator">
                  <div className="recording-dot"></div>
                  Recording in progress...
                </div>
              )}
            </div>

            <div className="interview-actions">
              {currentQuestion < questions.length - 1 ? (
                <button
                  onClick={handleNextQuestion}
                  disabled={recordings.length <= currentQuestion}
                  className="btn btn-primary"
                >
                  Next Question
                </button>
              ) : (
                <button
                  onClick={handleCompleteInterview}
                  disabled={recordings.length < questions.length}
                  className="btn btn-success"
                >
                  <CheckCircle size={20} />
                  Complete Interview
                </button>
              )}
            </div>
          </div>
        )}

        {/* Results View */}
        {currentView === "results" && results && (
          <div className="results-view">
            <div className="results-header">
              <h2 className="results-title">Interview Results</h2>

              <div className="stats-grid">
                <div className="stat-card stat-primary">
                  <h3>Overall Score</h3>
                  <div className="stat-value">{results.overallScore}%</div>
                </div>
                <div className="stat-card stat-success">
                  <h3>Questions Answered</h3>
                  <div className="stat-value">{results.answers.length}</div>
                </div>
              </div>

              <div className="summary-section">
                <h3>Summary</h3>
                <p className="summary-text">{results.summary}</p>
              </div>
            </div>

            <div className="analysis-section">
              <h3>Question-by-Question Analysis</h3>
              <div className="answers-list">
                {results.answers.map((answer, index) => (
                  <div key={index} className="answer-item">
                    <h4 className="answer-question">
                      Q{index + 1}: {answer.question}
                    </h4>
                    <p className="answer-text">{answer.answer}</p>
                    <div className="answer-metrics">
                      <span className="metric">
                        <Clock size={16} />
                        {answer.duration}
                      </span>
                      <span
                        className={`metric confidence ${getConfidenceClass(
                          answer.confidence
                        )}`}
                      >
                        <Star size={16} />
                        {getConfidenceLabel(answer.confidence)} Confidence (
                        {answer.confidence}%)
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="improvements-section">
              <h3>Improvement Suggestions</h3>
              <ul className="improvements-list">
                {results.improvements.map((tip, index) => (
                  <li key={index} className="improvement-item">
                    <div className="improvement-bullet"></div>
                    <p>{tip}</p>
                  </li>
                ))}
              </ul>
            </div>

            <div className="results-actions">
              <button
                onClick={() => {
                  setCurrentView("home");
                  setCurrentQuestion(0);
                  setRecordings([]);
                  setResults(null);
                  setInterviewData({
                    jobDescription: "",
                    companyName: "",
                    yearsExperience: "",
                    interviewType: "technical",
                  });
                }}
                className="btn btn-primary btn-large"
              >
                Start New Interview
              </button>
            </div>
          </div>
        )}
      </main>

      {/* Dialog */}
      {showDialog && (
        <div className="dialog-overlay">
          <div className="dialog">
            <h3 className="dialog-title">Interview Setup</h3>

            <div className="form-group">
              <label className="form-label">Job Description *</label>
              <textarea
                value={interviewData.jobDescription}
                onChange={(e) =>
                  setInterviewData((prev) => ({
                    ...prev,
                    jobDescription: e.target.value,
                  }))
                }
                className="form-input form-textarea"
                rows="3"
                placeholder="Enter the job description or key requirements..."
              />
            </div>

            <div className="form-group">
              <label className="form-label">Company Name *</label>
              <input
                type="text"
                value={interviewData.companyName}
                onChange={(e) =>
                  setInterviewData((prev) => ({
                    ...prev,
                    companyName: e.target.value,
                  }))
                }
                className="form-input"
                placeholder="Enter company name..."
              />
            </div>

            <div className="form-group">
              <label className="form-label">Years of Experience *</label>
              <input
                type="number"
                value={interviewData.yearsExperience}
                onChange={(e) =>
                  setInterviewData((prev) => ({
                    ...prev,
                    yearsExperience: e.target.value,
                  }))
                }
                className="form-input"
                placeholder="Enter years of experience..."
                min="0"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Interview Type</label>
              <select
                value={interviewData.interviewType}
                onChange={(e) =>
                  setInterviewData((prev) => ({
                    ...prev,
                    interviewType: e.target.value,
                  }))
                }
                className="form-input form-select"
              >
                <option value="technical">Technical</option>
                <option value="hr">HR</option>
              </select>
            </div>

            <div className="dialog-actions">
              <button
                onClick={() => setShowDialog(false)}
                className="btn btn-secondary"
              >
                Cancel
              </button>
              <button
                onClick={handleGenerateInterview}
                className="btn btn-primary"
              >
                Generate Interview
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIInterviewApp;
