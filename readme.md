# 🚀 PlacementBuddy – AI-Powered Resume Analysis & Job Match Platform

PlacementBuddy is an **AI-driven career assistant** that helps students and job seekers improve their resumes, analyze strengths, get ATS scores, and match resumes with job descriptions — all through a clean and modern interface.

This project consists of:

- ✨ **Next.js 14 (App Router) Frontend**
- ⚡ **FastAPI Backend**
- 🤖 **AI Resume Analysis using OpenAI**
- 📄 **Cloudinary Resume Upload**
- 🧠 **ATS Score Calculation**
- 🎯 **Job Description Match**
- 🔒 **JWT Authentication**
- 📚 **MongoDB + Beanie ODM**

---

## ⭐ Features

### 📤 Resume Upload
- Upload PDF/DOCX resumes
- Stored securely on Cloudinary
- Auto-extract text and metadata
- Live preview using iframe viewer

### 🧠 AI Resume Analysis
- Uses OpenAI to analyze:
  - Resume quality  
  - Missing improvements  
  - Skill insights  
  - Top weaknesses & suggestions  
- Analysis is saved → reused instantly next time

### 🔍 ATS Score System
Automatic checks for:
- Missing sections  
- Email/phone detection  
- Resume length  
- Skill coverage  
- Structure & formatting issues  

### 🎯 Job Description Match
- Paste a job description
- AI compares resume with JD
- Provides:
  - Match percentage  
  - Missing skills  
  - Matching skills  
  - Suggested improvements  

### 🔐 Authentication
- Secure JWT login system
- Protected API routes
- Frontend protected pages

### 📊 Dashboard
Includes:
- Resume preview  
- “Analyze Resume” / “View Analysis” button  
- JD Match input  
- Match results + skill gap  

---

## 🏗 Tech Stack

### **Frontend**
- Next.js 14 (App Router)
- TypeScript
- TailwindCSS
- Axios
- LocalStorage auth
- Cloudinary PDF viewer
- Vercel (recommended)

### **Backend**
- FastAPI (Python)
- MongoDB + Beanie ODM
- OpenAI API
- Cloudinary SDK
- pdfplumber + docx parser
- JWT (Jose)
- Uvicorn

---

