
from validator import validate
from corpus import CORPUS
import copy


def test_determinism():
    for sentence in CORPUS:
        r1 = validate(copy.deepcopy(sentence))
        r2 = validate(copy.deepcopy(sentence))
        assert r1 == r2, "Determinism violated"


def test_structural_rejection():
    invalid = {
        "intent": "Transfer",
        "context": {"balance": 1000},
        "constraints": [{"field": "balance", "value": 5000}],
        "outcome": "Allowed"
    }

    result = validate(invalid)
    assert result["classification"] == "Rejected (Structural)"


def test_constraint_order_preserved():
    sentence = {
        "actor": "User",
        "intent": "Test",
        "context": {"x": 1, "y": 2},
        "constraints": [
            {"field": "x", "value": 1},
            {"field": "y", "value": 999}
        ],
        "outcome": "Refused",
        "reason": {"field": "y", "value": 999}
    }

    result = validate(sentence)
    assert result["classification"] == "Accepted + Refused"


if __name__ == "__main__":
    test_determinism()
    test_structural_rejection()
    test_constraint_order_preserved()
    print("All compliance tests passed.")



















# python main.py sample_allowed.json
# python main.py sample_refused.json
# python main.py sf01_missing_actor.json
# python main.py drift_outcome_manipulation.json