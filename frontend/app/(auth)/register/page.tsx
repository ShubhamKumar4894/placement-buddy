import RegisterForm from "@/components/RegisterForm";
import Link from "next/link";
const Register = () => {
  return (
    <div className="w-full max-w-md bg-[#0d1224] p-8 rounded-2xl shadow-xl border border-white/10">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Create an Account
      </h1>

      <RegisterForm />

      <p className="mt-6 text-center text-gray-400">
        Already have an account?{" "}
        <Link href="/auth/login" className="text-[var(--neon)] hover:underline">
          Login
        </Link>
      </p>
    </div>
  );
};

export default Register;
