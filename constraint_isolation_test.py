import copy
import json
import hashlib
from validator import validate


# --------------------------------------------
# Utility: Deterministic Hash
# --------------------------------------------

def hash_object(obj: dict) -> str:
    serialized = json.dumps(obj, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


# --------------------------------------------
# Constraint Isolation Validation
# --------------------------------------------

def test_context_immutability():

    original_sentence = {
        "actor": "User_001",
        "intent": "Transfer",
        "context": {
            "balance": 5000,
            "verified": True
        },
        "constraints": [
            {"field": "verified", "value": True},
            {"field": "balance", "value": 5000}
        ],
        "outcome": "Allowed"
    }

    # Deep copy snapshot
    snapshot = copy.deepcopy(original_sentence)

    # Hash before validation
    before_hash = hash_object(original_sentence)

    # Run validator
    validate(original_sentence)

    # Hash after validation
    after_hash = hash_object(original_sentence)

    # Structural equality check
    assert original_sentence == snapshot, \
        "Input sentence was mutated."

    # Hash equality check
    assert before_hash == after_hash, \
        "Input hash changed during validation."

    print("Context immutability verified.")


# --------------------------------------------
# Additional Semantic Mutation Attempt
# --------------------------------------------

def test_constraint_list_immutability():

    sentence = {
        "actor": "User_002",
        "intent": "Transfer",
        "context": {"balance": 1000},
        "constraints": [
            {"field": "balance", "value": 5000}
        ],
        "outcome": "Refused",
        "reason": {"field": "balance", "value": 5000}
    }

    snapshot = copy.deepcopy(sentence)
    validate(sentence)

    assert sentence == snapshot, \
        "ConstraintSet mutated during evaluation."

    print("Constraint immutability verified.")


# --------------------------------------------
# Run Isolation Tests
# --------------------------------------------

if __name__ == "__main__":

    test_context_immutability()
    test_constraint_list_immutability()

    print("Constraint isolation validation passed.")
