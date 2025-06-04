def validate_schema(data, required_fields):
    anomalies = []
    for field, expected_type in required_fields.items():
        if field not in data:
            anomalies.append(f"Missing required field: {field}.")
        elif not isinstance(data[field], expected_type):
            anomalies.append(
                f"Type mismatch for field '{field}': Expected {expected_type.__name__}, got {type(data[field]).__name__}."
            )
    return anomalies
