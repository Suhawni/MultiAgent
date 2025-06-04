from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import shutil
from uuid import uuid4
import json

from app.classifier_agent import classify_input
from app.email_agent import process_email
from app.json_agent import process_json
from app.pdf_agent import process_pdf
from app.memory_store import MemoryStore
from app.action_router import route_action

from app.utils.file_parser import detect_format

app = FastAPI()
memory = MemoryStore()  

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(file_path, "rb") as f:
        content_bytes = f.read()

    file_type = detect_format(file_path)

    classification = classify_input(file.filename, content_bytes)

    memory.log_metadata({
        "filename": file.filename,
        "file_type": file_type,
        "business_intent": classification.get("intent")
    })

    result = {}
    if file_type == "email":
        result = process_email(content_bytes, memory)
        result["type"] = "email"

    elif file_type == "json":
        text_content = content_bytes.decode("utf-8")
        result = process_json(text_content, memory)
        result["type"] = "json"
        memory.log_agent_output("json", result)

    elif file_type == "pdf":
        result = process_pdf(file_path, memory)
        result["type"] = "pdf"
        memory.log_agent_output("pdf", result)

    action = await route_action(result, memory)
    result["action"] = action
    memory.log_agent_output("router", {"action": action})

    return JSONResponse(content=result)


@app.post("/crm/escalate")
def crm_escalate(payload: dict):
    """
    Simulate a CRM escalation endpoint.
    In a real scenario, this would be a separate service.
    """
    return {"status": "escalated", "details": payload}
