"use client";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import { useAuth } from "@/context/AuthContext";

export default function HomePage() {
  const router = useRouter();
  const { user } = useAuth();
  console.log(user);
  return (
    <main className="flex flex-col items-center justify-center min-h-screen text-center p-8">
      <Image
        src="/pngegg.png"
        alt="Placement Buddy Logo"
        width={120}
        height={120}
        className="shadow-md mb-6"
        priority
      />
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-2xl"
      >
        <h1 className="text-4xl font-bold mb-6 text-gray-900">
          Welcome to <span className="text-blue-600">Placement Buddy</span>
        </h1>

        <p className="text-lg text-gray-700 mb-10 leading-relaxed">
          Placement Buddy is your one-stop platform to manage your placement
          journey. Upload resumes, get AI-driven insights, and stay organized
          throughout your preparation. Whether you’re just starting or
          fine-tuning your resume, Placement Buddy helps you shine in every
          interview.
        </p>

        {user && user.token ? (
          <div className="flex flex-col items-center gap-6">
            <h2 className="text-2xl font-semibold text-gray-800">
              👋 Welcome, <span className="text-blue-600">{user.username}</span>
              !
            </h2>

            <Button
              onClick={() => router.push("/resume")}
              className="px-8 py-3 text-lg"
            >
              Go to Resume
            </Button>
          </div>
        ) : (
          <div className="flex justify-center gap-6">
            <Button
              onClick={() => router.push("/register")}
              className="px-8 py-3 text-lg"
            >
              Register
            </Button>

            <Button
              variant="outline"
              onClick={() => router.push("/login")}
              className="px-8 py-3 text-lg"
            >
              Sign In
            </Button>
          </div>
        )}
      </motion.div>
    </main>
  );
}
