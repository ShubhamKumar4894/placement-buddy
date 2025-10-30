"use client";
import { useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import AnalysisOverview from "@/components/analysis/AnalysisOverview";
import SkillCategories from "@/components/analysis/SkillCategories";
import FeedbackSection from "@/components/analysis/FeedbackSection";
import TopSuggestions from "@/components/analysis/TopSuggestions";
import toast from "react-hot-toast";
import { useEffect } from "react";
const ResumeAnalysisPage = () => {
  const searchParams = useSearchParams();
  const dataParam = searchParams.get("data");
  const data = dataParam ? JSON.parse(decodeURIComponent(dataParam)) : null;
  const results = data?.results;

  if (!results) {
    return (
      <p className="text-center mt-20 text-gray-600">No analysis data found.</p>
    );
  }
  useEffect(()=>{
    toast.success("Analysis completed!");
  },[])
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-5xl mx-auto space-y-8"
      >
        <h1 className="text-3xl font-bold text-center text-blue-700 mb-8">
          📊 Resume Analysis Report
        </h1>

        <AnalysisOverview results={results} />
        <SkillCategories categories={results.skill_categories} />
        <FeedbackSection sections={results.feedback_sections} />
        <TopSuggestions suggestions={results.top_suggestions} />
      </motion.div> 
    </main>
  );
};

export default ResumeAnalysisPage;
