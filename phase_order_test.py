from validator import validate


def test_phase_order_allowed():

    sentence = {
        "actor": "User_001",
        "intent": "Transfer",
        "context": {"balance": 5000},
        "constraints": [
            {"field": "balance", "value": 5000}
        ],
        "outcome": "Allowed"
    }

    result = validate(sentence, return_phase_log=True)

    assert result["phase_log"] == ["Structural", "Semantic", "Resolution"], \
        f"Invalid phase order: {result}"

    print("Allowed case phase order verified.")


def test_phase_order_structural_reject():

    sentence = {
        "intent": "Transfer",
        "context": {"balance": 1000},
        "constraints": [
            {"field": "balance", "value": 5000}
        ],
        "outcome": "Allowed"
    }

    result = validate(sentence, return_phase_log=True)

    assert result["phase_log"] == ["Structural"], \
        f"Invalid structural phase order: {result}"

    print("Structural rejection phase order verified.")


if __name__ == "__main__":
    test_phase_order_allowed()
    test_phase_order_structural_reject()
    print("Phase order enforcement verified.")
