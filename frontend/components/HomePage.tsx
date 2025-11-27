"use client";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import Link from "next/link";
export default function HomePage() {
  const router = useRouter();
  const { user,isAuthenticated } = useAuth();
  console.log(user);
  return (
    <main className="min-h-screen w-full  bg-[var(--navy)] text-white">
      <section className="container-main flex flex-col md:flex-row items-center justify-between py-20 gap-10">
        <div className="flex-1 space-y-6">
          <div className="inline-block px-4 py-1 rounded-full bg-[var(--neon)]/10 border border-[var(--neon)]/40 text-[var(--neon)] text-sm font-semibold">
            AI-Powered Resume Toolkit
          </div>
          <h1 className="text-4xl md:text-6xl font-bold leading-tight">
            Build a Resume That <br />
            <span className="text-[var(--neon)]">Gets You Interviews</span>
          </h1>
          <p className="text-gray-300 text-lg md:text-xl max-w-3xl">
            PlacementBuddy helps you analyze your resume, improve ATS score, and
            match it instantly with any job description — powered by advanced
            AI.
          </p>

          {!isAuthenticated && <div className="flex gap-4 mt-8">
            <Link
              href="/register"
              className="px-6 py-3 rounded-lg bg-[var(--neon)] text-black font-semibold hover:opacity-90"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="px-6 py-3 rounded-lg border border-[var(--neon)] text-[var(--neon)] hover:bg-[var(--neon)] hover:text-black transition"
            >
              Login
            </Link>
          </div>}
          {
            isAuthenticated && <div className="flex gap-4 mt-8">
            <Link
              href="/dashboard"
              className="px-6 py-3 rounded-lg bg-[var(--neon)] text-black font-semibold hover:opacity-90"
            >
              Go to Dashboard
            </Link>
          </div>
          }
        </div>
        
      </section>
      <section className="container-main py-24 px-8 md:px-20 text-center">
        <h2 className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-[var(--neon)] to-[var(--electric)] text-transparent bg-clip-text">
          Simple Steps to an Optimized Resume
        </h2>
        <p className="mt-4 text-gray-300 text-lg italic">
          Optimize your resume & land more interviews with PlacementBuddy
        </p>

        <div className="mt-16 flex flex-col md:flex-row items-center justify-between gap-16 relative">
          <div className="hidden md:block absolute top-[38px] left-0 right-0 h-[2px] bg-gradient-to-r from-pink-500 via-orange-400 to-pink-500 opacity-70 z-0"></div>
          <div className="flex flex-col items-center max-w-xs mx-auto relative z-10">
            <div className="w-16 h-16 rounded-full bg-pink-600 shadow-lg flex items-center justify-center text-2xl font-bold text-white">
              1
            </div>
            <h3 className="mt-6 text-xl font-semibold">Upload your resume</h3>
            <p className="mt-2 text-gray-400">
              Quickly upload your existing resume document.
            </p>
          </div>
          <div className="flex flex-col items-center max-w-xs mx-auto relative z-10">
            <div className="w-16 h-16 rounded-full bg-pink-600 shadow-lg flex items-center justify-center text-2xl font-bold text-white">
              2
            </div>
            <h3 className="mt-6 text-xl font-semibold">
              Paste the job description
            </h3>
            <p className="mt-2 text-gray-400">
              Provide any job description instantly.
            </p>
          </div>
          <div className="flex flex-col items-center max-w-xs mx-auto relative z-10">
            <div className="w-16 h-16 rounded-full bg-pink-600 shadow-lg flex items-center justify-center text-2xl font-bold text-white">
              3
            </div>
            <h3 className="mt-6 text-xl font-semibold">Get Instant Insights</h3>
            <p className="mt-2 text-gray-400">
              Receive AI insights for better optimization.
            </p>
          </div>
          <div className="flex flex-col items-center max-w-xs mx-auto relative z-10">
            <div className="w-16 h-16 rounded-full bg-pink-600 shadow-lg flex items-center justify-center text-2xl font-bold text-white">
              4
            </div>
            <h3 className="mt-6 text-xl font-semibold">Apply Smarter</h3>
            <p className="mt-2 text-gray-400">
              Submit an optimized resume personalized to the job.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
