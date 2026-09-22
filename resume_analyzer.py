"""Resume analysis engine: text extraction, ATS scoring, company & role recommendations."""

import os
from PyPDF2 import PdfReader

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

REQUIRED_SKILLS = [
    "python", "java", "javascript", "react", "html", "css", "sql",
    "machine learning", "ai", "fastapi", "mongodb", "cybersecurity",
    "docker", "aws", "data analysis", "tensorflow", "node.js",
]

COMPANY_DATABASE = {
    "Google": ["python", "machine learning", "ai"],
    "Microsoft": ["react", "sql", "python", "azure"],
    "Amazon": ["java", "sql", "aws"],
    "Infosys": ["html", "css", "javascript", "java"],
    "IBM": ["ai", "python", "data analysis"],
    "Wipro": ["cybersecurity", "python"],
    "TCS": ["java", "python", "sql"],
    "Meta": ["react", "javascript", "python"],
    "Netflix": ["java", "python", "aws"],
    "Accenture": ["sql", "javascript", "ai"],
}


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    if ext == ".pdf":
        reader = PdfReader(file_path)
        return " ".join(page.extract_text() or "" for page in reader.pages)
    if ext == ".docx":
        if HAS_DOCX:
            doc = Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs)
        return ""
    return ""


def analyze_resume_text(resume_text: str) -> dict:
    text = resume_text.lower()

    matched_skills = [s for s in REQUIRED_SKILLS if s in text]
    missing_skills = [s for s in REQUIRED_SKILLS if s not in text]

    if not matched_skills:
        return {
            "ats_score": 0,
            "status": "Rejected",
            "rejected": True,
            "matched_skills": [],
            "missing_skills": missing_skills[:8],
            "recommended_companies": [],
            "recommended_roles": [],
            "feedback": "Resume rejected — no technical skills detected. Add skills such as Python, Java, SQL, or React.",
        }

    ats_score = int((len(matched_skills) / len(REQUIRED_SKILLS)) * 100)
    if "project" in text:
        ats_score += 10
    if "internship" in text:
        ats_score += 10
    if "certification" in text or "certified" in text:
        ats_score += 5
    ats_score = min(ats_score, 100)

    if ats_score >= 80:
        status = "Highly Selected"
    elif ats_score >= 60:
        status = "Selected"
    elif ats_score >= 40:
        status = "Moderate Match"
    else:
        status = "Needs Improvement"

    recommended_companies = []
    for company, skills in COMPANY_DATABASE.items():
        if any(skill in text for skill in skills):
            recommended_companies.append(company)
    if not recommended_companies:
        recommended_companies = ["Infosys", "TCS", "Wipro"]

    recommended_roles = []
    if "python" in text or "fastapi" in text:
        recommended_roles.append("Python Developer")
    if "machine learning" in text or "ai" in text or "tensorflow" in text:
        recommended_roles.append("Machine Learning Engineer")
    if "react" in text or "javascript" in text or "html" in text:
        recommended_roles.append("Frontend Developer")
    if "cybersecurity" in text:
        recommended_roles.append("Cybersecurity Analyst")
    if "sql" in text or "data analysis" in text:
        recommended_roles.append("Data Analyst")
    if "python" in text and "react" in text:
        recommended_roles.append("Full Stack Developer")
    if not recommended_roles:
        recommended_roles.append("Software Developer")

    if ats_score >= 80:
        feedback = "Excellent resume with strong ATS score and relevant skills."
    elif ats_score >= 60:
        feedback = "Good resume. Add more projects to strengthen your profile."
    else:
        feedback = "Add more technical skills, projects, and certifications."

    return {
        "ats_score": ats_score,
        "status": status,
        "rejected": False,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills[:8],
        "recommended_companies": recommended_companies,
        "recommended_roles": recommended_roles,
        "feedback": feedback,
    }


def format_resume(name, email, phone, skills, education, projects, experience="") -> str:
    return f"""{name}
{email} | {phone} 

EDUCATION
{education}

SKILLS
{skills}

EXPERIENCE
{experience or "— Add your experience here —"}

PROJECTS
{projects}
"""
