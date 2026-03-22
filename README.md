# ResumeCraft AI — Resume Tailor

A Flask web app powered by Claude AI to tailor your resume to any Job Description — without changing your format, template, or logic.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key
```bash
export GROQ_API_KEY=your_key_here
```

### 3. Run the app
```bash
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

---

## Features

| Step | Tool | What it does |
|------|------|-------------|
| 1 | JD Analysis | Extracts must-have skills, ATS keywords, seniority signals |
| 2 | Gap Analysis | ATS score, missing keywords, undersold experiences |
| 3 | Bullet Optimizer | Rewrites bullets with JD keywords (no fake experience) |
| 4 | Summary Optimizer | Aligns your summary to the target role |
| 5 | Sanity Check | Ensures format/structure is preserved |

---

## Project Structure
```
resume_tailor/
├── app.py              # Flask backend + Claude API
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Full frontend UI
└── README.md
```
