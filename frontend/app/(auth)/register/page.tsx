import RegisterForm from "@/components/RegisterForm";
import Link from "next/link";
const Register = () => {
  return (
    <div>
      <div className="mb-4 flex flex-col items-center justify-center">
        <h1 className="text-3xl items-center font-bold text-blue-600 mb-2">
          WELCOME!
        </h1>
        <p className="text-blue-400">Try placement buddy now!</p>
      </div>
      <RegisterForm />
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600">
          Already a user?{" "}
          <Link
            href="/login"
            className="text-blue-600 font-semibold hover:underline"
          >
            Login
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
