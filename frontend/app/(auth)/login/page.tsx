import LoginForm from "@/components/LoginForm";

const Login = () => {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--navy)] px-4">
      <div className="w-full max-w-md bg-[#0d1224] p-8 rounded-2xl shadow-xl border border-white/10">
        {/* Heading */}
        <h1 className="text-3xl font-bold text-center">Welcome Back</h1>
        <p className="text-gray-400 text-center mt-2">
          Login to continue to{" "}
          <span className="text-[var(--neon)]">PlacementBuddy</span>
        </p>

        {/* Form */}
        <div className="mt-8">
          <LoginForm />
        </div>

        {/* Footer Link */}
        <p className="mt-6 text-center text-gray-400">
          New user?{" "}
          <a
            href="/auth/register"
            className="text-[var(--neon)] hover:underline"
          >
            Create an account
          </a>
        </p>
      </div>
    </div>
  );
};

export default Login;
