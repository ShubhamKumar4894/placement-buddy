"use client";
import { useAuth } from "@/context/AuthContext";
import Link from "next/link";

export default function Navbar() {
  const { isAuthenticated, logout, user } = useAuth();

  return (
    <header className="w-full border-b border-white/10 bg-[var(--navy)] backdrop-blur-lg sticky top-0 z-50">
      <nav className="container-main flex items-center justify-between py-4">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-[var(--neon)]/20 border border-[var(--neon)]/40 flex items-center justify-center">
            <span className="text-[var(--neon)] font-bold text-lg">P</span>
          </div>

          <Link href="/">
            <h1 className="text-2xl font-bold tracking-tight">
              <span className="text-white">Placement</span>
              <span className="text-[var(--neon)]">Buddy</span>
            </h1>
          </Link>
        </div>

        {/* Right Section */}
        {!isAuthenticated ? (
          <div className="flex items-center gap-4">
            <Link
              href="/login"
              className="text-gray-300 hover:text-white transition"
            >
              Login
            </Link>

            <Link
              href="/register"
              className="px-4 py-2 rounded-lg bg-[var(--neon)] text-black font-semibold hover:opacity-80 transition"
            >
              Signup
            </Link>
          </div>
        ) : (
          <div className="flex items-center gap-6">
            <p className="text-gray-300 text-sm font-semibold">Hi, {user?.username}!</p>

            <button
              onClick={logout}
              className="px-4 py-2 rounded-lg bg-red-500 text-white font-semibold hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        )}
      </nav>
    </header>
  );
}
