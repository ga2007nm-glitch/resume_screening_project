"""AI Resume Screening System — FastAPI backend."""

import asyncio
import json
import os
import shutil

from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from dashboard import get_dashboard_data, record_analysis
from notifications import add_notification, get_notifications, get_unread_count, mark_read, mark_all_read
from resume_analyzer import analyze_resume_text, extract_text, format_resume

# Ensure required directories exist
os.makedirs("uploads", exist_ok=True)

# ── App Initialization & Middleware ────────────────────────────────────────

app = FastAPI(title="AI Resume Screening System")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# ── Helper Functions ───────────────────────────────────────────────────────

def render(request: Request, template: str, page: str, title: str):
    """Unified rendering helper to keep layout contexts consistent."""
    return templates.TemplateResponse(
        request=request,
        name=template,
        context={"page": page, "title": title},
    )

def _notify_analysis(result: dict) -> None:
    """Helper to process notifications based on ATS score status."""
    status = result.get("status", "Completed")
    score = result.get("ats_score", 0)
    ntype = "warning" if result.get("rejected") or score < 60 else "success"
    add_notification("Resume Analyzed", f"ATS Score: {score}% — {status}", ntype)

# ── HTML Pages ─────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return render(request, "index.html", "home", "Home")

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return render(request, "about.html", "about", "About")

@app.get("/screening", response_class=HTMLResponse)
def screening(request: Request):
    return render(request, "screening.html", "screening", "Resume Screening")

@app.get("/sample-resume", response_class=HTMLResponse)
def generator(request: Request):
    return render(request, "generator.html", "generator", "Resume Generator")

@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return render(request, "contact.html", "contact", "Contact")

@app.get("/notifications", response_class=HTMLResponse)
def notifications_page(request: Request):
    return render(request, "notifications.html", "notifications", "Notifications")

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return render(request, "dashboard.html", "dashboard", "Dashboard")


# ── API Endpoints ──────────────────────────────────────────────────────────

@app.get("/api/dashboard")
def dashboard_data():
    return get_dashboard_data()

@app.get("/api/dashboard-stream")
async def dashboard_stream():
    async def event_generator():
        while True:
            yield f"data: {json.dumps(get_dashboard_data())}\n\n"
            await asyncio.sleep(2)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/notifications")
def notifications_data():
    return {"notifications": get_notifications(), "unread_count": get_unread_count()}

@app.post("/api/notifications/read/{note_id}")
def notification_mark_read(note_id: int):
    mark_read(note_id)
    return {"ok": True}

@app.post("/api/notifications/read-all")
def notification_mark_all_read():
    mark_all_read()
    return {"ok": True}

@app.post("/api/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text(file_path)
    if not resume_text.strip():
        return JSONResponse(status_code=400, content={"error": "Could not read resume. Upload PDF or TXT."})

    result = analyze_resume_text(resume_text)
    record_analysis(result["ats_score"], result["status"])
    _notify_analysis(result)
    return result

@app.post("/api/analyze-text")
async def analyze_text(text: str = Form(...)):
    if not text.strip():
        return JSONResponse(status_code=400, content={"error": "Resume text is empty."})

    result = analyze_resume_text(text)
    record_analysis(result["ats_score"], result["status"])
    _notify_analysis(result)
    return result

@app.post("/api/generate-resume")
async def generate_resume(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    skills: str = Form(...),
    education: str = Form(...),
    projects: str = Form(...),
    experience: str = Form(""),
):
    resume_text = format_resume(name, email, phone, skills, education, projects, experience)
    add_notification("Resume Generated", f"Resume created for {name}", "info")
    return {"message": "Resume Generated Successfully", "resume_text": resume_text}

@app.post("/api/contact")
async def submit_contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    add_notification("New Contact Message", f"From {name}: {message[:80]}...", "info")
    return {"message": "Thank you! We will get back to you soon."}