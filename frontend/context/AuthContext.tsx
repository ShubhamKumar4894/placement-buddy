"use client";
import {
  createContext,
  useState,
  useEffect,
  useContext,
  ReactNode,
} from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { User, AuthContextType } from "@/types/auth";

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const storedUser = localStorage.getItem("placementbuddy_user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);
  const registerUser = async (
    username: string,
    email: string,
    password: string
  ) => {
    try {
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth/register`, {
        username,
        email,
        password,
      });
      router.push("/");
    } catch (error: any) {
      console.error(
        "Registration failed:",
        error.response?.data || error.message
      );
    }
  };
  const login = async (email: string, password: string) => {
    try {
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/auth/login`,
        { email, password }
      );
      setIsAuthenticated(true);
      const loggedUser = {
        email,
        token: res.data.access_token,
        isAuthenticated: true,
        username: res.data.user.full_name
      };
      localStorage.setItem("placementbuddy_user", JSON.stringify(loggedUser));
      setUser(loggedUser);
      router.push("/resume");
    } catch (error: any) {
      setIsAuthenticated(false);
      console.error("Login failed:", error.response?.data || error.message);
      alert("Invalid credentials. Please try again.");
    }
  };

  const logout = () => {
    localStorage.removeItem("placementbuddy_user");
    setUser(null);
    router.push("/");
  };
  return (
    <AuthContext.Provider
      value={{ user, login, logout, isAuthenticated, registerUser, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
