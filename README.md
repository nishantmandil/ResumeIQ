<div align="center">

# ✦ ResumeIQ

### AI-Powered Resume Tailoring Platform

**Match your resume to any job description — instantly, accurately, and without fabrication.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=flat-square)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

[Features](#-features) · [Demo](#-demo) · [Quick Start](#-quick-start) · [Usage](#-usage) · [Deploy](#-deployment) · [Tech Stack](#-tech-stack)

---

<img width="1892" height="918" alt="image" src="https://github.com/user-attachments/assets/4ddb4340-b000-4e6d-a778-be21982dc017" />


</div>

---

## 🧠 What is ResumeIQ?

ResumeIQ is a production-grade, AI-powered resume tailoring platform built for job seekers who want to **maximize their ATS scores** without compromising authenticity. Unlike generic resume tools, ResumeIQ uses a recruiter-grade AI system prompt trained on 10 years of HR and SRE hiring intelligence — rewording your experience to match job descriptions perfectly, while never fabricating skills or experience you don't have.

> **Zero hallucination. Maximum relevance.**

---

## ✨ Features

| Tool | What It Does |
|---|---|
| **🔍 JD Analysis** | Extracts must-have skills, ATS keywords, seniority signals, and red flags from any job description |
| **📊 Gap Analysis** | Scores your resume against the JD (0–100 ATS score) and identifies missing keywords and undersold experiences |
| **✍️ Bullet Optimizer** | Rewrites your work experience bullets to match JD keywords — same facts, smarter framing |
| **📝 Summary Optimizer** | Aligns your professional summary to the target role without changing your voice |
| **✅ Sanity Check** | Verifies your tailored resume is format-intact, consistent, and free from exaggerations |
| **📎 File Upload** | Upload PDF, DOCX, or TXT resumes — text extracted automatically |
| **⚡ Auto-fill** | One-click extraction of bullets and summary directly from your uploaded resume |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/resumeiq.git
cd resumeiq
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

> Get your free API key at [console.groq.com](https://console.groq.com) — no credit card required.

### 4. Run the app

```bash
python app.py
```

Open your browser at **[http://localhost:5000](http://localhost:5000)** 🎉

---

## 📖 Usage

### Step-by-Step Workflow

```
1. Upload Resume  →  2. Paste JD  →  3. Analyze  →  4. Optimize  →  5. Verify
```

**Step 1 — Add your resume**
Upload a PDF, DOCX, or TXT file using the drag-and-drop zone, or paste your resume text directly into the left panel.

**Step 2 — Add the job description**
Paste the complete job description into the right panel. Include responsibilities, requirements, and skills for best results.

**Step 3 — JD Analysis (Tab 1)**
Click **Analyze JD** to extract must-have skills, ATS keywords, seniority signals, and any red flags from the job description.

**Step 4 — Gap Analysis (Tab 2)**
Run a full gap analysis to get your ATS score, identify missing keywords, and receive instant reword suggestions.

**Step 5 — Optimize Bullets (Tab 3)**
Click **⚡ Auto-fill** to pull your work experience bullets from your resume automatically, then click **Optimize Bullets** to get AI-rewritten versions with JD keywords naturally embedded.

**Step 6 — Optimize Summary (Tab 4)**
Auto-fill your current summary and optimize it for the target role — same tone, better alignment.

**Step 7 — Sanity Check (Tab 5)**
Paste your final tailored resume and run a sanity check to verify format integrity, section completeness, and consistency score before submitting.

---

## 📁 Project Structure

```
resumeiq/
│
├── app.py                  # Flask backend — all API routes
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── .gitignore
├── README.md
│
└── templates/
    └── index.html          # Full frontend — HTML + CSS + JS (single file)
```

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the main application |
| `POST` | `/upload-resume` | Parses uploaded PDF / DOCX / TXT |
| `POST` | `/extract-section` | Auto-extracts bullets or summary from resume text |
| `POST` | `/analyze` | Analyzes a job description for keywords and signals |
| `POST` | `/gap-analysis` | Compares resume vs JD, returns ATS score |
| `POST` | `/optimize-bullets` | Rewrites bullet points with JD keywords |
| `POST` | `/optimize-summary` | Rewrites professional summary for target role |
| `POST` | `/sanity-check` | Compares original vs tailored resume for integrity |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10, Flask 3.0 |
| **AI Model** | LLaMA 3.3 70B via Groq API |
| **PDF Parsing** | PyPDF2 |
| **DOCX Parsing** | python-docx |
| **Frontend** | Vanilla HTML/CSS/JS (zero dependencies) |
| **Typography** | Playfair Display · Outfit · JetBrains Mono |
| **Environment** | python-dotenv |

### Why Groq?

Groq's LPU inference engine delivers **~10× faster responses** than standard LLM APIs — making real-time resume tailoring feel instant rather than sluggish. LLaMA 3.3 70B is used for its superior instruction-following and consistent JSON output.

---

## 🌐 Deployment

### PythonAnywhere (Recommended — Free Forever)

1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Upload your files via the **Files** tab or clone from GitHub:
   ```bash
   git clone https://github.com/yourusername/resumeiq.git
   ```
3. Install dependencies in the Bash console:
   ```bash
   pip3 install --user flask groq python-dotenv PyPDF2 python-docx
   ```
4. Go to **Web** tab → **Add new web app** → **Flask** → **Python 3.10**
5. Edit the WSGI file:
   ```python
   import sys, os
   project_home = '/home/yourusername/resumeiq'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)
   from dotenv import load_dotenv
   load_dotenv(os.path.join(project_home, '.env'))
   from app import app as application
   ```
6. Add `GROQ_API_KEY` in the **Environment Variables** section
7. Click **Reload** → Live at `yourusername.pythonanywhere.com` ✅

> ⚠️ PythonAnywhere free tier restricts outbound internet. Test Groq API access with `curl https://api.groq.com` in their Bash console first.

---

### Render.com (Free — Always On Option)

1. Add a `Procfile` to your project root:
   ```
   web: gunicorn app:app
   ```
2. Add `gunicorn` to `requirements.txt`
3. Push to GitHub
4. Connect repo on [render.com](https://render.com) → **New Web Service**
5. Set `GROQ_API_KEY` in environment variables
6. Deploy ✅

> Free tier sleeps after 15 min of inactivity. Upgrade to $7/mo for always-on.

---

### Local Development

```bash
# Clone
git clone https://github.com/yourusername/resumeiq.git
cd resumeiq

# Install
pip install -r requirements.txt

# Configure
echo "GROQ_API_KEY=your_key_here" > .env

# Run
python app.py
# → http://localhost:5000
```

---

## ⚙️ Configuration

All configuration is handled via the `.env` file:

```env
# Required
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx

# Optional — change the AI model (default: llama-3.3-70b-versatile)
# GROQ_MODEL=llama-3.3-70b-versatile
```

### Switching AI Models

To use a different Groq model, edit line 14 in `app.py`:

```python
GROQ_MODEL = "llama-3.3-70b-versatile"   # default — best quality
GROQ_MODEL = "llama-3.1-8b-instant"      # faster, lighter
GROQ_MODEL = "mixtral-8x7b-32768"        # longer context window
```

---

## 🔒 Privacy & Ethics

- **No data storage** — your resume and JD are never saved to a database or disk
- **No fabrication** — the AI system prompt explicitly prohibits adding skills or experience you don't have
- **No tracking** — zero analytics, cookies, or third-party scripts
- **Local-first** — all processing happens server-side per request; nothing persists between sessions

---

## 📦 Dependencies

```txt
flask>=3.0.0          # Web framework
groq>=0.9.0           # Groq API client (LLaMA inference)
python-dotenv>=1.0.0  # Environment variable management
PyPDF2>=3.0.0         # PDF text extraction
python-docx>=1.1.0    # DOCX text extraction
gunicorn              # Production WSGI server (for deployment)
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# Fork the repo, then:
git clone https://github.com/yourusername/resumeiq.git
cd resumeiq
git checkout -b feature/your-feature-name

# Make your changes, then:
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
# Open a Pull Request
```

### Ideas for contributions
- [ ] LinkedIn summary optimizer  
- [ ] Multi-language support
- [ ] Resume scoring history / session persistence
- [ ] Dark/light mode toggle
- [ ] Export tailored resume as PDF

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — for blazing-fast LLM inference
- [Meta AI](https://ai.meta.com) — for the LLaMA 3.3 model
- [Flask](https://flask.palletsprojects.com) — for the lightweight web framework
- [Google Fonts](https://fonts.google.com) — Playfair Display, Outfit, JetBrains Mono

---

<div align="center">

**Built with ♥ for job seekers everywhere**

*ResumeIQ — Your resume, perfectly aligned.*

⭐ Star this repo if it helped you land an interview!

</div>
