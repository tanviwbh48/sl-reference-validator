def evaluate_constraints(constraints: list, context: dict) -> dict:
    if not isinstance(constraints, list):
        raise ValueError("ConstraintSet must be a list")

    for index, constraint in enumerate(constraints):

        if not isinstance(constraint, dict):
            raise ValueError("Invalid constraint structure")

        if "field" not in constraint or "value" not in constraint:
            raise ValueError("Constraint must contain field and value")

        field = constraint["field"]
        expected = constraint["value"]

        if field not in context:
            return {
                "status": "Failed",
                "failed_constraint": constraint,
                "failed_index": index
            }

        actual = context[field]

        if actual != expected:
            return {
                "status": "Failed",
                "failed_constraint": constraint,
                "failed_index": index
            }

    return {
        "status": "Satisfied",
        "failed_constraint": None,
        "failed_index": None
    }
