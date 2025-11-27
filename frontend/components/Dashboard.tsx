"use client";
import React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import Link from "next/link";
import LoadingSpinner from "./LoadingSpinner";

export default function Dashboard() {
  const [resume, setResume] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [jdLoading, setJdLoading] = useState(false);
  const [jobDesc, setJobDesc] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [matchResult, setMatchResult] = useState<any>(null);

  useEffect(() => {
    const stored = localStorage.getItem("placementbuddy_user");
    const token = stored ? JSON.parse(stored).token : null;

    if (!token) {
      window.location.href = "/login";
      return;
    }

    axios
      .get("http://127.0.0.1:8000/api/v1/resume/my", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        console.log(res.data.resumes);
        setResume(res.data.resumes[0]); // take first resume for now
      })
      .finally(() => setLoading(false));
  }, []);

  const handleJDMatch = async () => {
    const stored = localStorage.getItem("placementbuddy_user");
    const token = stored ? JSON.parse(stored).token : null;

    if (!token) return alert("Not authenticated");
    if (!resume?.analysis_id) return alert("Please analyze your resume first!");

    setJdLoading(true);
    setMatchResult(null);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/v1/resume/match",
        {
          job_description: jobDesc,
          analysis_id: resume.analysis_id,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setMatchResult(res.data.match_result);
    } catch (error: any) {
      console.error(error);
      alert("Failed to match JD.");
    } finally {
      setJdLoading(false);
    }
  };

  const handleButtonClick = async () => {
    const stored = localStorage.getItem("placementbuddy_user");
    const token = stored ? JSON.parse(stored).token : null;

    if (!token) return alert("Not authenticated");

    try {
      setAnalyzing(true);
      const res = await axios.post(
        `http://127.0.0.1:8000/api/v1/resume/analyze/${resume._id}`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      localStorage.setItem("resume_analysis", JSON.stringify(res.data));
      window.location.href = `/analysis/${res.data.analysis_id}`;
    } catch (error: any) {
      console.error(error);
      alert("Failed to analyze resume.");
    } finally {
      setAnalyzing(false);
    }
  };
  if (analyzing) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-[var(--navy)] text-white px-6 md:px-20 py-12">
      {/* PAGE TITLE */}
      <h1
        className="text-4xl md:text-5xl font-bold mb-10 text-center bg-gradient-to-r 
      from-[var(--neon)] via-white to-[var(--neon)]
      bg-clip-text text-transparent"
      >
        Your Dashboard
      </h1>

      <div className="grid md:grid-cols-2 gap-10">
        <div
          className="bg-[#0e132d] border border-white/10 p-8 rounded-2xl shadow-xl 
             hover:border-[var(--neon)]/40 transition flex flex-col gap-6"
        >
          <h2 className="text-2xl font-semibold text-[var(--neon)]">
            Your Resume
          </h2>

          {!resume ? (
            <>
              <p className="text-gray-400 mb-4">No resume uploaded yet.</p>

              <a
                href="/upload"
                className="px-5 py-3 bg-[var(--neon)] text-black rounded-lg font-semibold hover:opacity-90"
              >
                Upload Resume
              </a>
            </>
          ) : (
            <>
              <div className="w-full flex justify-center">
                <iframe
                  src={`https://docs.google.com/gview?url=${resume.file_url}&embedded=true`}
                  className="w-full h-64 rounded-lg border border-white/10 shadow-lg"
                ></iframe>
              </div>

              <p className="text-gray-300">
                <strong>File:</strong> {resume.filename}
              </p>

              <div className="flex gap-4 mt-2">
                <a
                  href={resume.file_url}
                  target="_blank"
                  className="px-4 py-2 border border-[var(--neon)] text-[var(--neon)] 
                     rounded-lg hover:bg-[var(--neon)] hover:text-black transition"
                >
                  View Resume
                </a>

                <button
                  onClick={handleButtonClick}
                  className="px-4 py-2 bg-[var(--neon)] text-black rounded-lg 
                     font-semibold hover:opacity-90"
                >
                  View Analysis
                </button>
              </div>
            </>
          )}
        </div>
        {resume && (
          <div
            className="bg-[#0e132d] border border-white/10 p-8 rounded-2xl shadow-xl 
                hover:border-[var(--neon)]/40 transition"
          >
            <h2 className="text-2xl font-semibold mb-4 text-[var(--neon)]">
              Job Description Match
            </h2>

            <p className="text-gray-400 mb-2">Paste a job description below:</p>

            <textarea
              value={jobDesc}
              onChange={(e) => setJobDesc(e.target.value)}
              rows={6}
              className="w-full mt-3 p-4 rounded-lg bg-white/5 border border-white/20 
                 text-white outline-none focus:border-[var(--neon)] transition"
              placeholder="Paste job description here..."
            />

            <button
              onClick={handleJDMatch}
              disabled={jdLoading}
              className={`mt-4 w-full px-5 py-3 rounded-lg font-semibold transition
        ${
          jdLoading
            ? "bg-gray-500 text-black opacity-50 cursor-not-allowed"
            : "bg-[var(--neon)] text-black hover:opacity-90"
        }`}
            >
              {jdLoading ? "Matching..." : "Match with Resume"}
            </button>

            {/* Match Result */}
            {matchResult && (
              <div className="mt-6 border border-[var(--neon)]/40 p-5 rounded-xl bg-white/5 backdrop-blur">
                <h3 className="text-2xl font-semibold text-[var(--neon)] mb-2">
                  Match Score: {matchResult.match_percentage}%
                </h3>

                <p className="text-gray-300 mb-4">
                  {matchResult.alignment_summary}
                </p>

                <h4 className="font-semibold text-white mt-3">
                  Matching Skills
                </h4>
                <ul className="list-disc ml-6 text-gray-400">
                  {matchResult.matching_skills.map((s: string, i: number) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>

                <h4 className="font-semibold text-white mt-4">
                  Missing Skills
                </h4>
                <ul className="list-disc ml-6 text-gray-400">
                  {matchResult.missing_skills.map((s: string, i: number) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>

                <h4 className="font-semibold text-white mt-4">
                  Suggested Improvements
                </h4>
                <ul className="list-disc ml-6 text-gray-400">
                  {matchResult.suggested_improvements.map(
                    (s: string, i: number) => (
                      <li key={i}>{s}</li>
                    )
                  )}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
