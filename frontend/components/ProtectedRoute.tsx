"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user,loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && (!user || !user.token)) {
      router.push("/login");
    }
  }, [user, loading, router]);
  
  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user || !user.token) {
    return null; 
  }

  return <>{children}</>;
}
