import json
from app.utils.schema_validator import validate_schema

REQUIRED_SCHEMA = {
    "name": str,
    "intent": str,
    "version": int,
}

def process_json(content, memory):
    try:
        data = json.loads(content)
        anomalies = validate_schema(data, REQUIRED_SCHEMA)

        result = {
            "type": "json",
            "data": data,
            "anomalies": anomalies
        }

        if anomalies:
            memory.log_alert("json", anomalies)
        memory.log_agent_output("json", result)
        return result

    except json.JSONDecodeError as e:
        memory.log_alert("json", f"Invalid JSON: {str(e)}")
        return {"error": "Invalid JSON"}
