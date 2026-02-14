from grammar import (
    REQUIRED_PRIMITIVES,
    OPTIONAL_PRIMITIVES,
    CANONICAL_ORDER,
    VALID_OUTCOMES
)


# --------------------------------------------
# Structural Validation Error (Taxonomy-Aware)
# --------------------------------------------

class StructuralValidationError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


# --------------------------------------------
# Canonical Order Enforcement
# --------------------------------------------

def check_canonical_order(sentence: dict) -> None:
    keys = list(sentence.keys())

    expected_order = [
        key for key in CANONICAL_ORDER
        if key in sentence
    ]

    if keys != expected_order:
        raise StructuralValidationError(
            "SF-04",
            "Canonical primitive order violated"
        )


# --------------------------------------------
# Structural Validation Engine (S1–S20)
# --------------------------------------------

def validate_structure(sentence: dict) -> None:

    # -------- S1–S5: Mandatory Primitive Presence --------
    for primitive in REQUIRED_PRIMITIVES:
        if primitive not in sentence:
            raise StructuralValidationError(
                "SF-01",
                f"Missing required primitive: {primitive}"
            )

    # -------- Unknown Primitive Detection --------
    valid_primitives = set(REQUIRED_PRIMITIVES + OPTIONAL_PRIMITIVES)
    for key in sentence.keys():
        if key not in valid_primitives:
            raise StructuralValidationError(
                "SF-11",
                f"Unknown primitive: {key}"
            )

    # -------- Primitive Type Enforcement --------
    if not isinstance(sentence["actor"], str):
        raise StructuralValidationError(
            "SF-08",
            "Actor must be string"
        )

    if not isinstance(sentence["intent"], str):
        raise StructuralValidationError(
            "SF-08",
            "Intent must be string"
        )

    if not isinstance(sentence["context"], dict):
        raise StructuralValidationError(
            "SF-08",
            "Context must be dictionary"
        )

    # -------- S8–S12: Canonical Order --------
    check_canonical_order(sentence)

    # -------- S20: Outcome Domain Check --------
    outcome = sentence["outcome"]

    if outcome not in VALID_OUTCOMES:
        raise StructuralValidationError(
            "SF-07",
            "Invalid outcome value"
        )

    # -------- S6–S7: Conditional Reason Rules --------
    if outcome == "Refused" and "reason" not in sentence:
        raise StructuralValidationError(
            "SF-03",
            "Reason required when outcome is Refused"
        )

    if outcome == "Allowed" and "reason" in sentence:
        raise StructuralValidationError(
            "SF-03",
            "Reason forbidden when outcome is Allowed"
        )

    # -------- S17: Reason Multiplicity --------
    if isinstance(sentence.get("reason"), list):
        raise StructuralValidationError(
            "SF-06",
            "Multiple reasons not allowed"
        )

    # -------- S13–S16: Cardinality / Duplicate Keys --------
    if len(set(sentence.keys())) != len(sentence.keys()):
        raise StructuralValidationError(
            "SF-05",
            "Duplicate primitive detected"
        )

    # -------- S2: ConstraintSet Integrity --------
    constraints = sentence["constraints"]

    if not isinstance(constraints, list):
        raise StructuralValidationError(
            "SF-09",
            "ConstraintSet must be list"
        )

    if len(constraints) == 0:
        raise StructuralValidationError(
            "SF-02",
            "ConstraintSet must not be empty"
        )

    # -------- S18: Constraint Structural Integrity --------
    for constraint in constraints:

        if not isinstance(constraint, dict):
            raise StructuralValidationError(
                "SF-08",
                "Constraint must be dictionary"
            )

        if "field" not in constraint or "value" not in constraint:
            raise StructuralValidationError(
                "SF-08",
                "Constraint missing field or value"
            )

    # -------- S10: Primitive Nesting / Interleaving --------
    for key, value in sentence.items():
        if isinstance(value, dict):
            for nested_key in value.keys():
                if nested_key in REQUIRED_PRIMITIVES:
                    raise StructuralValidationError(
                        "SF-10",
                        "Primitive nesting detected"
                    )
