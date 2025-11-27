"use client";
import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import toast from "react-hot-toast";
const RegisterForm = () => {
  const [loading, setLoading] = useState(false);
  const { registerUser } = useAuth();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      await registerUser(form.username, form.email, form.password);
      toast.success("Registration successful! now login with your credentials");
      window.location.href = "/dashboard";
    } catch (error) {
      console.error(error);
      toast.error("Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Username */}
      <input
        type="text"
        name="username"
        placeholder="Username"
        value={form.username}
        onChange={handleChange}
        className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/20 focus:border-[var(--neon)] outline-none"
      />

      {/* Email */}
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={form.email}
        onChange={handleChange}
        className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/20 focus:border-[var(--neon)] outline-none"
      />

      {/* Password */}
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={form.password}
        onChange={handleChange}
        className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/20 focus:border-[var(--neon)] outline-none"
      />

      <button
        type="submit"
        disabled={loading}
        className="w-full px-4 py-3 rounded-lg bg-[var(--neon)] text-black font-semibold hover:opacity-90 transition"
      >
        {loading ? "Creating Account..." : "Sign Up"}
      </button>
    </form>
  );
};

export default RegisterForm;
