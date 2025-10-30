"use client";
import { useState } from "react";
import {useRouter} from "next/navigation";
import LoadingSpinner from "@/components/LoadingSpinner";
import { Button } from "@/components/ui/button";
import ProtectedRoute from "@/components/ProtectedRoute";
const ResumePage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [uploaded, setUploaded] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const router=useRouter();
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (!selected) return;

    setFile(selected);
    setPreviewUrl(URL.createObjectURL(selected));

    // Start parsing immediately
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", selected);
      const userData = localStorage.getItem("placementbuddy_user");
      if (!userData) return alert("Please login first!");

      const { token } = JSON.parse(userData);
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/resume/upload`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
          credentials: "include",
        }
      );

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      setData(data);
      console.log("✅ Resume parsed and uploaded:", data);
      setUploaded(true);
    } catch (err: any) {
      console.error("Upload error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  const handleRemove = async () => {
    const { file_path } = data;
    if (!file_path) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const userData = localStorage.getItem("placementbuddy_user");
      if (!userData) return alert("Please login first!");

      const { token } = JSON.parse(userData);

      const response = await fetch(
        `${
          process.env.NEXT_PUBLIC_API_URL
        }/resume/delete?file_path=${encodeURIComponent(file_path)}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          credentials: "include",
        }
      );

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to delete file");
      }
      console.log("✅ Resume deleted successfully");
      setFile(null);
      setPreviewUrl(null);
      setUploaded(false);
      setData(null);
    } catch (err: any) {
      console.error("Delete error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    const { resume_id } = data;
    if (!resume_id) {
      return alert("Please upload a resume first!");
    }
    setLoading(true);
    setError(null);
    try {
      const userData = localStorage.getItem("placementbuddy_user");
      if (!userData) return alert("Please login first!");
      const { token } = JSON.parse(userData);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/resume/analyze/${resume_id}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to analyze resume.");
      }

      const data = await response.json();
     
      router.push(
        `/resume/analysis?data=${encodeURIComponent(JSON.stringify(data))}`
      );
    } catch (err: any) {
      console.error("Analyze error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <main className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
        <div className="max-w-3xl w-full bg-white rounded-2xl shadow-lg p-8">
          <h1 className="text-3xl font-bold text-center text-blue-600 mb-3">
            Get a Free Instant AI Resume Review
          </h1>
          <p className="text-gray-600 text-center mb-8">
            Upload your resume and let Placement Buddy analyze it for
            improvements, missing keywords, and overall impact.
          </p>

          {/* Upload Section */}
          {!file && (
            <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 p-10 rounded-xl hover:bg-gray-50 transition">
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={handleFileChange}
                className="hidden"
                id="resume-upload"
              />
              <label
                htmlFor="resume-upload"
                className="cursor-pointer bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition"
              >
                Upload Resume
              </label>
              <p className="text-sm text-gray-500 mt-3">
                Supported formats: PDF, DOCX
              </p>
            </div>
          )}

          {/* Loading Spinner */}
          {loading && (
            <div className="mt-6 flex justify-center">
              <LoadingSpinner text="Processing your resume..." />
            </div>
          )}

          {/* Preview and Analyze Section */}
          {uploaded && !loading && (
            <div className="mt-6 space-y-4">
              <div className="flex items-center justify-between">
                <p className="font-medium text-gray-700 truncate w-3/4">
                  {file?.name}
                </p>

                <Button
                  variant="outline"
                  onClick={handleRemove}
                  disabled={loading}
                >
                  {loading ? "Removing..." : "Remove"}
                </Button>
              </div>

              {/* Resume Preview */}
              {previewUrl && (
                <div className="border rounded-lg overflow-hidden h-[500px] bg-gray-100">
                  <iframe
                    src={previewUrl}
                    className="w-full h-full"
                    title="Resume Preview"
                  />
                </div>
              )}

              {/* Analyze Button */}
              <div className="flex justify-center">
                <Button
                  onClick={handleAnalyze}
                  className="bg-green-600 hover:bg-green-700 text-white px-8 py-2 text-lg"
                >
                  Analyze Resume
                </Button>
              </div>

              {/* Error message */}
              {error && (
                <p className="text-red-500 text-center mt-2">{error}</p>
              )}
            </div>
          )}
        </div>
      </main>
    </ProtectedRoute>
  );
};

export default ResumePage;
