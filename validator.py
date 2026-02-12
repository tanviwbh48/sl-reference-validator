from structural import validate_structure, StructuralValidationError
from semantic import evaluate_constraints
from resolution import resolve
from phase_tracker import PhaseTracker


def validate(sentence: dict, return_phase_log: bool = False) -> dict:

    tracker = PhaseTracker()

    # ----------------------------
    # Phase 1 — Structural
    # ----------------------------
    tracker.enter("Structural")

    try:
        validate_structure(sentence)

    except StructuralValidationError as e:
        tracker.verify_sequence()

        result = {
            "classification": "Rejected (Structural)",
            "failure_class": e.code,
            "message": e.message
        }

        if return_phase_log:
            result["phase_log"] = tracker.phases

        return result

    # ----------------------------
    # Phase 2 — Semantic
    # ----------------------------
    tracker.enter("Semantic")

    evaluation_result = evaluate_constraints(
        sentence["constraints"],
        sentence["context"]
    )

    # ----------------------------
    # Phase 3 — Resolution
    # ----------------------------
    tracker.enter("Resolution")

    resolution_result = resolve(evaluation_result)

    tracker.verify_sequence()

    if return_phase_log:
        resolution_result["phase_log"] = tracker.phases

    return resolution_result
