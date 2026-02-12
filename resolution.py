def resolve(evaluation_result: dict) -> dict:
    if evaluation_result["status"] == "Satisfied":
        return {
            "classification": "Accepted + Allowed"
        }

    return {
        "classification": "Accepted + Refused",
        "reason": evaluation_result["failed_constraint"]
    }
