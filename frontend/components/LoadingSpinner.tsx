"use client";
import React from "react";
interface LoadingSpinnerProps {
  size?: number; 
  text?: string; 
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = () => {
  return (
    <div className="min-h-screen bg-[var(--navy)] text-white flex justify-center items-center">
      <div className="animate-spin h-14 w-14 border-4 border-[var(--neon)] border-t-transparent rounded-full"></div>
    </div>
  );
};

export default LoadingSpinner;
