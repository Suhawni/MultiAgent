import re
import pdfplumber

def extract_invoice_total(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    match = re.search(r'Total\s*[:\-]?\s*\$?\s*([0-9,]+\.?[0-9]*)', text, re.IGNORECASE)
    total = 0.0
    if match:
        total = float(match.group(1).replace(",", ""))

    lower_text = text.lower()
    if any(keyword in lower_text for keyword in ["invoice", "amount due", "billing", "payment"]):
        doc_type = "invoice"
    elif any(keyword in lower_text for keyword in ["policy", "compliance", "regulation", "gdpr", "fda", "hipaa"]):
        doc_type = "policy"
    else:
        doc_type = "unknown"

    return {
        "type": doc_type,
        "total": total,
        "text": text
    }


def check_compliance_mentions(text):
    flags = []
    upper_text = text.upper()
    if "GDPR" in upper_text:
        flags.append("GDPR")
    if "FDA" in upper_text:
        flags.append("FDA")
    if "HIPAA" in upper_text:
        flags.append("HIPAA")
    return flags
