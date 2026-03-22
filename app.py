from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import json
import os
import io

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a 10-year experienced HR and SRE recruiter and resume coach.
Your job is to help candidates tailor their resumes to job descriptions WITHOUT:
- Changing the original format or template
- Adding fake experience or skills they don't have
- Altering the logical flow or structure
- Changing the overall tone/voice of the candidate

You think like both a recruiter AND an ATS system. You know exactly what hiring managers
for SRE, DevOps, Platform Engineering, and tech roles look for.

IMPORTANT: Always respond with valid JSON only. No markdown, no extra text, no explanation."""

def call_groq(prompt, max_tokens=4096):
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=max_tokens,
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt}
        ]
    )
    return response.choices[0].message.content

def clean_json(text):
    return text.strip().replace("```json", "").replace("```", "").strip()

def extract_text_from_pdf(file_bytes):
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except ImportError:
        return None

def extract_text_from_docx(file_bytes):
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return text.strip()
    except ImportError:
        return None

# ── Home ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ── Upload Resume ─────────────────────────────────────────────────────
@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded."})
    file       = request.files['file']
    filename   = file.filename.lower()
    file_bytes = file.read()
    extracted  = None

    if filename.endswith('.txt'):
        try:
            extracted = file_bytes.decode('utf-8')
        except Exception as e:
            return jsonify({"success": False, "error": f"Could not read TXT: {e}"})
    elif filename.endswith('.pdf'):
        extracted = extract_text_from_pdf(file_bytes)
        if extracted is None:
            return jsonify({"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"})
    elif filename.endswith('.docx'):
        extracted = extract_text_from_docx(file_bytes)
        if extracted is None:
            return jsonify({"success": False, "error": "python-docx not installed. Run: pip install python-docx"})
    else:
        return jsonify({"success": False, "error": "Unsupported file. Use PDF, DOCX, or TXT."})

    if not extracted or len(extracted.strip()) < 50:
        return jsonify({"success": False, "error": "Could not extract enough text. Try pasting manually."})

    return jsonify({"success": True, "text": extracted})

# ── Extract Section (Auto-fill) ───────────────────────────────────────
@app.route("/extract-section", methods=["POST"])
def extract_section():
    data    = request.json
    resume  = data.get("resume", "")
    section = data.get("section", "bullets")

    if not resume.strip():
        return jsonify({"success": False, "error": "No resume text provided."})

    if section == "bullets":
        prompt = f"""From this resume, extract ALL bullet points from the Work Experience section.

RESUME:
{resume}

Rules:
- Extract every bullet point exactly as written
- Include bullets from ALL jobs
- Prefix each line with a bullet •
- Return ONLY this JSON:
{{"extracted": "• bullet one\\n• bullet two\\n• bullet three"}}"""
    else:
        prompt = f"""From this resume, extract the professional summary, objective, or profile section.

RESUME:
{resume}

Rules:
- Return the text exactly as written
- If no summary exists, write a neutral 2-3 sentence summary from the resume content
- Return ONLY this JSON:
{{"extracted": "Summary text here..."}}"""

    try:
        result = call_groq(prompt, max_tokens=2000)
        parsed = json.loads(clean_json(result))
        return jsonify({"success": True, "text": parsed.get("extracted", "")})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ── JD Analysis ───────────────────────────────────────────────────────
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    jd   = data.get("jd", "")
    prompt = f"""Analyze this Job Description and extract:
1. Must-have technical skills
2. Good-to-have skills
3. Key ATS keywords
4. Seniority signals (lead, own, drive, architect)
5. Red flags or unusual requirements

Job Description:
{jd}

Return ONLY this JSON:
{{
  "must_have": ["skill1", "skill2"],
  "good_to_have": ["skill1", "skill2"],
  "ats_keywords": ["keyword1", "keyword2"],
  "seniority_signals": ["signal1", "signal2"],
  "red_flags": ["flag1", "flag2"]
}}"""
    try:
        result = call_groq(prompt)
        parsed = json.loads(clean_json(result))
        return jsonify({"success": True, "data": parsed})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ── Gap Analysis ──────────────────────────────────────────────────────
@app.route("/gap-analysis", methods=["POST"])
def gap_analysis():
    data   = request.json
    resume = data.get("resume", "")
    jd     = data.get("jd", "")
    prompt = f"""Do a detailed gap analysis between this resume and job description.

RESUME:
{resume}

JOB DESCRIPTION:
{jd}

Return ONLY this JSON:
{{
  "aligned_points": ["point1", "point2"],
  "missing_keywords": ["kw1", "kw2"],
  "undersold_experiences": ["exp1", "exp2"],
  "reword_suggestions": [
    {{"original": "original bullet", "suggested": "reworded bullet", "reason": "why"}}
  ],
  "ats_score": 72,
  "score_breakdown": {{
    "technical_match": 80,
    "keyword_density": 65,
    "seniority_match": 70,
    "overall": 72
  }}
}}"""
    try:
        result = call_groq(prompt)
        parsed = json.loads(clean_json(result))
        return jsonify({"success": True, "data": parsed})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ── Optimize Bullets ──────────────────────────────────────────────────
@app.route("/optimize-bullets", methods=["POST"])
def optimize_bullets():
    data     = request.json
    bullets  = data.get("bullets", "")
    jd       = data.get("jd", "")
    keywords = data.get("keywords", [])
    prompt = f"""Reword these resume bullet points to better match the JD.

RULES:
- Do NOT change meaning or add experience the candidate doesn't have
- Keep same format: action verb + task + result/metric
- Naturally include these keywords: {', '.join(keywords)}
- Do not change number of bullet points

BULLET POINTS:
{bullets}

JD CONTEXT:
{jd}

Return ONLY this JSON:
{{
  "optimized_bullets": [
    {{"original": "original text", "optimized": "reworded text", "keywords_added": ["kw1"]}}
  ]
}}"""
    try:
        result = call_groq(prompt)
        parsed = json.loads(clean_json(result))
        return jsonify({"success": True, "data": parsed})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ── Optimize Summary ──────────────────────────────────────────────────
@app.route("/optimize-summary", methods=["POST"])
def optimize_summary():
    data      = request.json
    summary   = data.get("summary", "")
    jd        = data.get("jd", "")
    job_title = data.get("job_title", "the role")
    prompt = f"""Rewrite this resume summary to align with the JD.

RULES:
- Do not add skills/experience the candidate doesn't have
- Keep it to 3-4 lines max
- Use JD keywords naturally
- Target role: {job_title}

CURRENT SUMMARY:
{summary}

JOB DESCRIPTION:
{jd}

Return ONLY this JSON:
{{
  "optimized_summary": "rewritten summary here",
  "keywords_included": ["kw1", "kw2"],
  "changes_made": ["change1", "change2"]
}}"""
    try:
        result = call_groq(prompt)
        parsed = json.loads(clean_json(result))
        return jsonify({"success": True, "data": parsed})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ── Sanity Check ──────────────────────────────────────────────────────
@app.route("/sanity-check", methods=["POST"])
def sanity_check():
    data     = request.json
    original = data.get("original", "")
    tailored = data.get("tailored", "")
    prompt = f"""Compare these two resumes and do a final sanity check.

ORIGINAL RESUME:
{original}

TAILORED RESUME:
{tailored}

Return ONLY this JSON:
{{
  "format_preserved": true,
  "sections_intact": true,
  "consistency_score": 90,
  "flags": [
    {{"section": "Summary", "status": "green", "note": "Looks good"}}
  ],
  "overall_rating": "green",
  "final_recommendations": ["rec1", "rec2"]
}}
Status values: green (good), yellow (minor issue), red (problem)"""
    try:
        result = call_groq(prompt)
        parsed = json.loads(clean_json(result))
        return jsonify({"success": True, "data": parsed})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)