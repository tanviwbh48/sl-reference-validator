import copy
import hashlib
import json
from validator import validate


# --------------------------------------------
# Determinism Harness (1000-Run Verification)
# --------------------------------------------


def hash_output(result: dict) -> str:
    """
    Produce deterministic hash of validator output.
    """
    serialized = json.dumps(result, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


def run_determinism_test(sentence: dict, iterations: int = 1000):
    """
    Runs identical input multiple times and verifies identical outputs.
    """

    baseline_result = validate(copy.deepcopy(sentence))
    baseline_hash = hash_output(baseline_result)

    for i in range(iterations):
        result = validate(copy.deepcopy(sentence))
        result_hash = hash_output(result)

        if result_hash != baseline_hash:
            raise Exception(
                f"Determinism violated at iteration {i}\n"
                f"Baseline: {baseline_result}\n"
                f"Current: {result}"
            )

    print(f"Determinism verified for {iterations} runs.")


# --------------------------------------------
# Test Sentences
# --------------------------------------------

VALID_ALLOWED = {
    "actor": "User_001",
    "intent": "Transfer",
    "context": {"balance": 5000},
    "constraints": [
        {"field": "balance", "value": 5000}
    ],
    "outcome": "Allowed"
}

VALID_REFUSED = {
    "actor": "User_002",
    "intent": "Transfer",
    "context": {"balance": 1000},
    "constraints": [
        {"field": "balance", "value": 5000}
    ],
    "outcome": "Refused",
    "reason": {"field": "balance", "value": 5000}
}

STRUCTURAL_INVALID = {
    "intent": "Transfer",
    "context": {"balance": 1000},
    "constraints": [
        {"field": "balance", "value": 5000}
    ],
    "outcome": "Allowed"
}


# --------------------------------------------
# Run Harness
# --------------------------------------------

if __name__ == "__main__":

    print("Testing Allowed case...")
    run_determinism_test(VALID_ALLOWED)

    print("Testing Refused case...")
    run_determinism_test(VALID_REFUSED)

    print("Testing Structural Rejection case...")
    run_determinism_test(STRUCTURAL_INVALID)

    print("All determinism tests passed.")
