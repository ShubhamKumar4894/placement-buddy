# Placement Buddy

**Placement Buddy** is an AI-powered resume evaluation and placement assistance web app.  
It analyzes uploaded resumes, extracts skills and experience using NLP, compares them with job descriptions, and provides smart feedback powered by **OpenAI GPT-4o**.

---

## 🚀 Project Overview

### 🔄 End-to-End Workflow

```text
1️⃣  User uploads resume (PDF)
     ↓
2️⃣  PyPDF2 / pdfplumber extracts raw text
     ↓
3️⃣  spaCy + Regex parse and identify structured sections
     ↓
4️⃣  Custom database extracts and matches relevant skills
     ↓
5️⃣  OpenAI GPT-4o analyzes and generates feedback
     ↓
6️⃣  Job match % is calculated from pasted job description
     ↓
7️⃣  Results are returned to frontend in real time

## 🧩 Features

✅ **AI-Powered Resume Analysis** — Uses GPT-4o to generate detailed resume feedback

✅ **Skill Extraction Engine** — spaCy + regex + database lookup for technical and soft skills

✅ **Job Match Scoring** — Compares resume content with a user-provided job description

✅ **Secure Authentication** — Email/password using JWT

✅ **Real-Time Feedback** — Fast API responses served to the Next.js frontend

✅ **Modern UI** — Clean, responsive interface built with TailwindCSS and TypeScript
```
