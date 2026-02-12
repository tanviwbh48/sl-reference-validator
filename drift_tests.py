from validator import validate
import copy


# --------------------------------------------
# Drift Injection Test Suite
# --------------------------------------------


def assert_structural(sentence, expected_sf):
    result = validate(sentence)

    assert result["classification"] == "Rejected (Structural)", \
        f"Expected structural rejection, got {result}"

    assert result["failure_class"] == expected_sf, \
        f"Expected {expected_sf}, got {result}"


def assert_refused(sentence):
    result = validate(sentence)

    assert result["classification"] == "Accepted + Refused", \
        f"Expected refusal, got {result}"


# --------------------------------------------
# Base Valid Sentence (Multi-Constraint)
# --------------------------------------------

BASE_MULTI = {
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


# --------------------------------------------
# 1. Constraint Reordering Attempt
# --------------------------------------------

def test_constraint_reordering():
    s = copy.deepcopy(BASE_MULTI)

    # Swap constraint order
    s["constraints"] = list(reversed(s["constraints"]))

    # Still valid structurally
    # But semantic must evaluate in declared order
    result = validate(s)

    assert result["classification"] == "Accepted + Allowed"


# --------------------------------------------
# 2. Multiple Reasons Injection
# --------------------------------------------

def test_multiple_reasons():
    s = copy.deepcopy(BASE_MULTI)
    s["outcome"] = "Refused"
    s["reason"] = [
        {"field": "balance", "value": 100},
        {"field": "verified", "value": False}
    ]

    assert_structural(s, "SF-06")


# --------------------------------------------
# 3. Outcome Manipulation (Allowed but failing constraint)
# --------------------------------------------

def test_allowed_with_failing_constraint():
    s = copy.deepcopy(BASE_MULTI)

    s["context"]["balance"] = 100  # force failure
    s["outcome"] = "Allowed"

    # Structural passes
    # Semantic must override and produce refusal
    result = validate(s)

    assert result["classification"] == "Accepted + Refused"


# --------------------------------------------
# 4. Missing Reason on Refusal
# --------------------------------------------

def test_missing_reason_on_refusal():
    s = copy.deepcopy(BASE_MULTI)
    s["outcome"] = "Refused"
    s.pop("reason", None)

    assert_structural(s, "SF-03")


# --------------------------------------------
# 5. Reason Provided but Constraint Actually Passes
# --------------------------------------------

def test_reason_when_constraints_pass():
    s = copy.deepcopy(BASE_MULTI)
    s["reason"] = {"field": "balance", "value": 999}

    assert_structural(s, "SF-03")


# --------------------------------------------
# 6. Constraint Corruption After Order
# --------------------------------------------

def test_constraint_corruption():
    s = copy.deepcopy(BASE_MULTI)
    s["constraints"] = [
        {"field": "verified", "value": True},
        "invalid"
    ]

    assert_structural(s, "SF-08")


# --------------------------------------------
# 7. Inject Unknown Primitive
# --------------------------------------------

def test_unknown_primitive():
    s = copy.deepcopy(BASE_MULTI)
    s["unknown"] = "bad"

    result = validate(s)

    # Should fail canonical order
    assert result["classification"] == "Rejected (Structural)"


# --------------------------------------------
# 8. Manipulate Reason Mismatch
# --------------------------------------------

def test_reason_not_matching_failed_constraint():
    s = copy.deepcopy(BASE_MULTI)

    s["context"]["balance"] = 100  # cause failure
    s["outcome"] = "Refused"
    s["reason"] = {"field": "verified", "value": True}

    result = validate(s)

    # Validator resolves based on first failure, not declared reason
    assert result["classification"] == "Accepted + Refused"


# --------------------------------------------
# 9. Attempt to Skip Constraints
# --------------------------------------------

def test_skip_constraints():
    s = copy.deepcopy(BASE_MULTI)
    s["constraints"] = []

    assert_structural(s, "SF-02")


# --------------------------------------------
# 10. Inject Nested Primitive
# --------------------------------------------

def test_nested_primitive():
    s = copy.deepcopy(BASE_MULTI)
    s["context"] = {"actor": "Injected"}

    assert_structural(s, "SF-10")


# --------------------------------------------
# Run All Drift Tests
# --------------------------------------------

if __name__ == "__main__":

    test_constraint_reordering()
    test_multiple_reasons()
    test_allowed_with_failing_constraint()
    test_missing_reason_on_refusal()
    test_reason_when_constraints_pass()
    test_constraint_corruption()
    test_unknown_primitive()
    test_reason_not_matching_failed_constraint()
    test_skip_constraints()
    test_nested_primitive()

    print("All drift injection tests passed.")
