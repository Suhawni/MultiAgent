import json
import PyPDF2
import re
import email
from email import message_from_bytes
import io

def classify_input(filename, content_bytes):
    # JSON
    if filename.endswith(".json"):
        try:
            content_str = content_bytes.decode("utf-8")
            data = json.loads(content_str)
            if "invoice_id" in data:
                return {"format": "JSON", "intent": "Invoice"}
            elif "alert_type" in data:
                return {"format": "JSON", "intent": "Fraud Risk"}
            else:
                return {"format": "JSON", "intent": "RFQ"}
        except:
            return {"format": "JSON", "intent": "Unknown"}

    # Email
    elif filename.endswith(".eml"):
        try:
            msg = message_from_bytes(content_bytes)
            subject = msg["subject"].lower() if msg["subject"] else ""
            if "invoice" in subject:
                intent = "Invoice"
            elif "regulation" in subject or "compliance" in subject:
                intent = "Regulation"
            elif "complaint" in subject or "angry" in subject:
                intent = "Complaint"
            else:
                intent = "RFQ"
            return {"format": "Email", "intent": intent}
        except:
            return {"format": "Email", "intent": "Unknown"}

    # PDF
    elif filename.endswith(".pdf"):
        try:
            pdf_file = io.BytesIO(content_bytes)
            reader = PyPDF2.PdfReader(pdf_file)
            text = "".join([p.extract_text() or "" for p in reader.pages])
            if "invoice" in text.lower():
                return {"format": "PDF", "intent": "Invoice"}
            elif re.search(r"GDPR|HIPAA|FDA", text, re.IGNORECASE):
                return {"format": "PDF", "intent": "Regulation"}
            else:
                return {"format": "PDF", "intent": "Unknown"}
        except:
            return {"format": "PDF", "intent": "Unknown"}

    return {"format": "Unknown", "intent": "Unknown"}
