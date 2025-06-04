import os
import json
import email
from email import policy
from email.parser import BytesParser
from PyPDF2 import PdfReader

def detect_format(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".eml":
        return "email"
    elif ext == ".json":
        return "json"
    elif ext == ".pdf":
        return "pdf"
    return "unknown"

def parse_email(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    return {
        "sender": msg["from"],
        "subject": msg["subject"],
        "body": msg.get_body(preferencelist=('plain')).get_content()
    }

def parse_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()
