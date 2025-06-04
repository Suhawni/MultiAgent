from app.utils.pdf_utils import extract_invoice_total, check_compliance_mentions

def process_pdf(file_path, memory):
    fields = extract_invoice_total(file_path)

    if not isinstance(fields, dict):
        result = {
            "type": "pdf",
            "fields": {},
            "risk_flag": True,
            "error": "Invalid format returned from extract_invoice_total"
        }
        memory.log_agent_output("pdf", result)
        return result

    risk_flag = False
    reasons = []

    if fields.get("type") == "invoice" and float(fields.get("total", 0)) > 10000:
        risk_flag = True
        reasons.append("High-value invoice over $10,000")

    if fields.get("type") == "policy":
        compliance_flags = check_compliance_mentions(fields.get("text", ""))
        if compliance_flags:
            risk_flag = True
            reasons.append(f"Mentions sensitive compliance terms: {', '.join(compliance_flags)}")
            fields["compliance_mentions"] = compliance_flags

    result = {
        "type": "pdf",
        "fields": fields,
        "risk_flag": risk_flag,
        "reasons": reasons
    }

    memory.log_agent_output("pdf", result)
    return result
