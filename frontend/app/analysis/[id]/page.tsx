"use client";

import { useEffect, useState } from "react";

export default function AnalysisPage() {
  const [analysis, setAnalysis] = useState<any>(null);

  useEffect(() => {
    const stored = localStorage.getItem("resume_analysis");
    if (stored) setAnalysis(JSON.parse(stored));
  }, []);

  if (!analysis)
    return (
      <p className="text-center text-white mt-20">
        No analysis found. Please analyze your resume first.
      </p>
    );

  const data = analysis.results;

  return (
    <div className="min-h-screen bg-[var(--navy)] text-white px-6 md:px-20 py-12">
      {/* PAGE TITLE */}
      <h1 className="text-4xl md:text-5xl font-bold text-center mb-12">
        Resume <span className="text-[var(--neon)]">Analysis</span>
      </h1>

      {/* SCORE SECTION */}
      <div className="grid md:grid-cols-2 gap-10 mb-10">
        {/* Overall Score */}
        <div className="bg-[#0e132d] p-8 rounded-2xl border border-white/10 shadow-xl text-center">
          <h2 className="text-xl text-gray-300 mb-2">Overall Score</h2>
          <p className="text-[var(--neon)] text-6xl font-bold">
            {data.overall_score}%
          </p>
        </div>

        {/* ATS Score */}
        <div className="bg-[#0e132d] p-8 rounded-2xl border border-white/10 shadow-xl text-center">
          <h2 className="text-xl text-gray-300 mb-2">ATS Score</h2>
          <p className="text-[var(--neon)] text-6xl font-bold">
            {data.ats_score}%
          </p>
        </div>
      </div>

      {/* TOP STRENGTHS + SUGGESTIONS */}
      <div className="grid md:grid-cols-2 gap-10 mb-10">
        {/* Strengths */}
        <div className="bg-[#0e132d] p-8 rounded-2xl border border-white/10 shadow-xl">
          <h3 className="text-2xl font-semibold mb-4 text-[var(--neon)]">
            Top Strengths
          </h3>

          <ul className="list-disc ml-5 text-gray-300 space-y-2">
            {data.top_strength?.map((s: string, i: number) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>

        {/* Suggestions */}
        <div className="bg-[#0e132d] p-8 rounded-2xl border border-white/10 shadow-xl">
          <h3 className="text-2xl font-semibold mb-4 text-[var(--neon)]">
            Top Suggestions
          </h3>

          <ul className="list-disc ml-5 text-gray-300 space-y-2">
            {data.top_suggestions?.map((s: string, i: number) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* FEEDBACK SECTIONS */}
      <h2 className="text-3xl font-bold mt-12 mb-6 text-center">
        Detailed Feedback
      </h2>

      <div className="grid md:grid-cols-2 gap-8">
        {data.feedback_sections?.map((section: any, idx: number) => (
          <div
            key={idx}
            className="bg-[#0e132d] p-8 rounded-2xl border border-white/10 shadow-lg"
          >
            <h3 className="text-2xl font-semibold text-[var(--neon)] mb-3">
              {section.category}
            </h3>

            <p className="text-gray-300 mb-2">
              <strong>Score:</strong> {section.score}%
            </p>

            <h4 className="text-white font-semibold mt-4">Strengths:</h4>
            <ul className="list-disc ml-5 text-gray-400">
              {section.strengths?.map((s: string, i: number) => (
                <li key={i}>{s}</li>
              ))}
            </ul>

            <h4 className="text-white font-semibold mt-4">Suggestions:</h4>
            <ul className="list-disc ml-5 text-gray-400">
              {section.suggestions?.map((s: string, i: number) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* ATS ANALYSIS SECTION */}
      <div className="mt-16 bg-[#0e132d] p-8 rounded-2xl border border-white/10 shadow-xl">
        <h2 className="text-3xl font-bold text-[var(--neon)] mb-4">
          ATS Analysis
        </h2>

        <p className="text-gray-300 mb-4">
          <strong>ATS Friendly:</strong>{" "}
          {data.ats_analysis.is_ats_friendly ? "Yes ✔" : "No ❌"}
        </p>

        <h3 className="font-semibold text-white mt-4">Issues:</h3>
        <ul className="list-disc ml-6 text-gray-400">
          {data.ats_analysis.issues?.map((i: string, idx: number) => (
            <li key={idx}>{i}</li>
          ))}
        </ul>

        <h3 className="font-semibold text-white mt-4">Recommendations:</h3>
        <ul className="list-disc ml-6 text-gray-400">
          {data.ats_analysis.recommendations?.map(
            (r: string, idx: number) => (
              <li key={idx}>{r}</li>
            )
          )}
        </ul>
      </div>
    </div>
  );
}
