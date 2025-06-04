def detect_tone(text):
    text = text.lower()
    if any(word in text for word in ["escalate", "immediately", "urgent", "asap"]):
        return "angry"
    if any(word in text for word in ["angry", "not happy", "frustrated", "complain", "terrible", "worst"]):
        return "angry"
    elif any(word in text for word in ["please", "kindly", "could you"]):
        return "polite"
    else:
        return "neutral"
