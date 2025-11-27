"use client";
import { AuthProvider } from "@/context/AuthContext";
import { Toaster } from "react-hot-toast";
import "./globals.css";
import Navbar from "@/components/ui/Navbar";
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
          <AuthProvider>
            <Navbar/>
            {children}
            <Toaster position="top-center" reverseOrder={false} />
          </AuthProvider>
        </div>
      </body>
    </html>
  );
}
