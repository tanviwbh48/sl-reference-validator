import json
import hashlib
import subprocess
import sys
import tempfile
import os


# --------------------------------------------
# Cross-Validator Consistency Script
# --------------------------------------------

def hash_output(output: dict) -> str:
    serialized = json.dumps(output, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


def run_external_instance(input_sentence: dict) -> dict:
    """
    Runs validator in a separate Python process.
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_file:
        json.dump(input_sentence, temp_file)
        temp_file_path = temp_file.name

    try:
        result = subprocess.run(
            [sys.executable, "main.py", temp_file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"Subprocess failed: {result.stderr}")

        output = json.loads(result.stdout)
        return output

    finally:
        os.remove(temp_file_path)


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
# Cross-Instance Consistency Test
# --------------------------------------------

def verify_cross_instance(sentence: dict):
    output1 = run_external_instance(sentence)
    output2 = run_external_instance(sentence)

    hash1 = hash_output(output1)
    hash2 = hash_output(output2)

    if hash1 != hash2:
        raise Exception(
            f"Inconsistent outputs detected\n"
            f"Output1: {output1}\n"
            f"Output2: {output2}"
        )

    print("Consistent hash:", hash1)


# --------------------------------------------
# Run Script
# --------------------------------------------

if __name__ == "__main__":

    print("Testing Allowed case...")
    verify_cross_instance(VALID_ALLOWED)

    print("Testing Refused case...")
    verify_cross_instance(VALID_REFUSED)

    print("Testing Structural case...")
    verify_cross_instance(STRUCTURAL_INVALID)

    print("Cross-validator consistency verified.")
