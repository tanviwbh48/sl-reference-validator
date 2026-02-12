CORPUS = [

    # Allowed
    {
        "actor": "User_001",
        "intent": "Transfer",
        "context": {"balance": 5000},
        "constraints": [
            {"field": "balance", "value": 5000}
        ],
        "outcome": "Allowed"
    },

    # Refused
    {
        "actor": "User_002",
        "intent": "Transfer",
        "context": {"balance": 1000},
        "constraints": [
            {"field": "balance", "value": 5000}
        ],
        "outcome": "Refused",
        "reason": {"field": "balance", "value": 5000}
    },

    # Structural Reject
    {
        "intent": "Transfer",
        "context": {"balance": 1000},
        "constraints": [
            {"field": "balance", "value": 5000}
        ],
        "outcome": "Allowed"
    }
]
