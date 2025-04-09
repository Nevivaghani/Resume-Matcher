from fastapi import APIRouter, UploadFile, File, Form
import os
from bson import ObjectId
import json

from app.services.resume_parser import load_resume
from app.services.matcher import match_resume_with_job

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_data: str = Form(...)  
):
    os.makedirs("resumes", exist_ok=True)

    file_path = f"resumes/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    docs = load_resume(file_path)
    resume_text = "\n".join([doc.page_content for doc in docs])

    try:
        job = json.loads(job_data)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON structure in job_data"}
    
    def clean_skills(skills):
        return [skill.strip() for skill in skills if isinstance(skill, str)]

    # Normalize keys for internal consistency

    job = {
        "job_title": job.get("job_title"),
        "primary_skills": clean_skills(job.get("primarySkills", [])),
        "secondary_skills": clean_skills(job.get("secondarySkills", [])),
        "project_skills": clean_skills(job.get("projectSkills", []))
    }
    print("@@@@@@@@@@@@ Parsed job object:", job)

    matched_jobs = match_resume_with_job(resume_text, [job])
    top_matches = matched_jobs[:1]

    for match in top_matches:
        if '_id' in match and isinstance(match['_id'], ObjectId):
            match['_id'] = str(match['_id'])

    return {"top_matched_jobs": top_matches}
