from email import message_from_bytes
from app.utils.tone_detector import detect_tone
import re

def process_email(content, memory):
    msg = message_from_bytes(content)
    sender = msg["from"]
    subject = msg["subject"]
    body = msg.get_payload()

    urgency = "high" if re.search(r"urgent|asap|immediately", body, re.IGNORECASE) else "low"
    issue = subject or "Unknown"
    tone = detect_tone(body)

    keywords = re.findall(r"\b(invoice|refund|compliance|delay|payment|complaint|regulation|fraud|cancel|reschedule)\b", body, re.IGNORECASE)
    keywords = list(set([k.lower() for k in keywords]))

    result = {
        "type": "email",
        "sender": sender,
        "urgency": urgency,
        "issue": issue,
        "tone": tone,
        "keywords": keywords
    }
    memory.log_agent_output("email", result)
    return result
