# Frozen Grammar Definitions

REQUIRED_PRIMITIVES = [
    "actor",
    "intent",
    "context",
    "constraints",
    "outcome"
]

OPTIONAL_PRIMITIVES = [
    "reason"
]

CANONICAL_ORDER = [
    "actor",
    "intent",
    "context",
    "constraints",
    "outcome",
    "reason"
]

VALID_OUTCOMES = {"Allowed", "Refused"}
