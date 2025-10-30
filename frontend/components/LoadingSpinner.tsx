"use client";
import React from "react";
interface LoadingSpinnerProps {
  size?: number; 
  text?: string; 
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 40, text }) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-3">
      <div
        className="animate-spin rounded-full border-4 border-blue-500 border-t-transparent"
        style={{ width: size, height: size }}
      />
      {text && <p className="text-gray-600 font-medium">{text}</p>}
    </div>
  );
};

export default LoadingSpinner;
