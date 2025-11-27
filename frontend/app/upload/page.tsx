"use client";

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

export default function UploadResume() {
  const router = useRouter();

  const [file, setFile] = useState<File | null>(null);
  const [previewURL, setPreviewURL] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploaded = e.target.files?.[0];
    setFile(uploaded || null);

    if (!uploaded) {
      setPreviewURL(null);
      return;
    }

    if (uploaded.type === "application/pdf") {
      setPreviewURL(URL.createObjectURL(uploaded));
    } else {
      setPreviewURL(null); // DOCX can’t be previewed
    }
  };

  const uploadResume = async () => {
    if (!file) {
      alert("Please select a resume!");
      return;
    }

    setUploading(true);

    const stored = localStorage.getItem("placementbuddy_user");
    const token = stored ? JSON.parse(stored).token : null;

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(
        "http://127.0.0.1:8000/api/v1/resume/upload",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );
      toast.success("Resume uploaded successfully!");

      router.push("/dashboard");
    } catch (err) {
      console.error(err);
      alert("Failed to upload resume. Try again!");
    }

    setUploading(false);
  };

  return (
    <div className="min-h-screen bg-[var(--navy)] text-white px-6 md:px-20 py-12">
      <h1 className="text-4xl md:text-5xl font-bold text-center bg-gradient-to-r 
      from-[var(--neon)] via-white to-[var(--neon)]
      bg-clip-text text-transparent mb-10">
        Upload Your Resume
      </h1>

      <div className="max-w-3xl mx-auto bg-[#0e132d] border border-white/10 p-8 rounded-2xl shadow-xl">
        <label className="block text-lg mb-3 font-semibold">
          Select Resume (PDF or DOCX)
        </label>

        <input
          type="file"
          accept=".pdf, .docx"
          onChange={handleFileChange}
          className="w-full p-3 bg-white/5 border border-white/20 rounded-lg text-gray-300 cursor-pointer"
        />

        {/* Preview Box */}
        <div className="mt-6">
          {file && (
            <div className="text-gray-300 mb-3">
              <strong>Selected File:</strong> {file.name}
            </div>
          )}

          {/* PDF Preview */}
          {previewURL && (
            <div className="mt-4">
              <iframe
                src={previewURL}
                className="w-full h-[500px] border border-[var(--neon)]/40 rounded-lg"
              />
            </div>
          )}

          {/* DOCX Preview Message */}
          {file && !previewURL && file.name.endsWith(".docx") && (
            <p className="text-gray-400 mt-3">
              Preview not available for DOCX files, but file is selected.
            </p>
          )}
        </div>

        <button
          onClick={uploadResume}
          disabled={uploading}
          className="mt-8 w-full px-5 py-3 bg-[var(--neon)] text-black rounded-lg 
                 font-semibold hover:opacity-90 transition"
        >
          {uploading ? "Uploading..." : "Upload Resume"}
        </button>
      </div>
    </div>
  );
}
