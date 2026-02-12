class PhaseTracker:
    VALID_SEQUENCE = ["Structural", "Semantic", "Resolution"]

    def __init__(self):
        self.phases = []

    def enter(self, phase_name: str):
        self.phases.append(phase_name)

    def verify_sequence(self):
        expected = self.VALID_SEQUENCE[:len(self.phases)]
        if self.phases != expected:
            raise Exception(
                f"Phase order violated. Expected {expected}, got {self.phases}"
            )
