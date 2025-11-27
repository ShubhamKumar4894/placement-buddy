"use client";
import { useAuth } from "@/context/AuthContext";
import { useState } from "react";
import toast from "react-hot-toast";
const LoginForm = () => {
  const { login } = useAuth();
  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(form.email, form.password);
      toast.success("Login successful!");
      window.location.href = "/dashboard"
    } catch (error) {
      console.error(error);
      toast.error("Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Email */}
      <input
        type="email"
        name="email"
        placeholder="Email"
        required
        value={form.email}
        onChange={handleChange}
        className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/20
                   focus:border-[var(--neon)] text-white outline-none transition"
      />

      {/* Password */}
      <input
        type="password"
        name="password"
        placeholder="Password"
        required
        value={form.password}
        onChange={handleChange}
        className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/20
                   focus:border-[var(--neon)] text-white outline-none transition"
      />

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className="w-full px-4 py-3 rounded-lg bg-[var(--neon)] text-black 
                   font-semibold hover:opacity-90 transition"
      >
        {loading ? "Logging in..." : "Login"}
      </button>
    </form>
  );
};

export default LoginForm;
