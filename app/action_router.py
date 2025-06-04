import httpx

async def notify_crm_escalate(result, memory):
    """
    Asynchronously call the CRM escalation endpoint.
    """
    url = "http://127.0.0.1:8000/crm/escalate"
    payload = {
        "sender": result.get("sender"),
        "issue": result.get("issue"),
        "tone": result.get("tone"),
        "urgency": result.get("urgency")
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
        # Log the response for audit
        memory.log_agent_output("crm", {"status_code": response.status_code, "response": response.json()})
        return response.json()
    except Exception as e:
        memory.log_alert("crm", str(e))
        return {"error": str(e)}

def notify_compliance(result, memory):
    """
    Synchronously simulate a call to the compliance team.
    """
    message = f"Compliance notified for JSON anomalies: {result.get('anomalies')}."
    memory.log_agent_output("compliance", message)
    print("[Compliance API] " + message)
    return message

async def route_action(result, memory):
    if result.get("type") == "email":
        if result.get("tone") == "angry" and result.get("urgency") == "high":
            escalation_response = await notify_crm_escalate(result, memory)
            return "POST /crm/escalate called: " + str(escalation_response)
        else:
            return "Log and close"

    elif result.get("type") == "json":
        if result.get("anomalies"):
            notify_compliance(result, memory)  
            return "Send to compliance team"
        return "Log transaction"

    elif result.get("type") == "pdf":
        if result.get("risk_flag"):
            return "Flag for review by risk department"
        return "Store in archive"

    return "No action required"
