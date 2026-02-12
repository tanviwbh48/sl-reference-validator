# 🧠 Sovereign Language Reference Validator
demo link:https://drive.google.com/file/d/1xgZjxGOJItwRreLrGH4N5nQsjVbGWdb0/view?usp=sharing
## Overview

This project implements a **deterministic reference validator** for the Sovereign Language.

The validator enforces:

- Frozen grammar
- Structural integrity
- Sequential constraint evaluation
- Deterministic outcome resolution
- Explicit structural failure taxonomy
- Drift resistance
- Phase order enforcement

The system validates intent sentences through strict validation phases without execution, inference, or mutation.

---

# 🎯 Purpose

The reference validator exists to:

- Validate Sovereign Language intent sentences
- Enforce structural grammar rules
- Evaluate constraints deterministically
- Produce exactly one outcome per sentence
- Prevent ambiguity, drift, or silent failure

The validator does **not execute actions** — it only validates and resolves.

---

# 🏗 System Architecture

The validator consists of independent components.

---

## 1. Structural Validation Layer (`structural.py`)

Responsible for grammar enforcement.

### Responsibilities
- Primitive presence validation
- Canonical order enforcement
- Primitive type validation
- Constraint structure validation
- Structural failure taxonomy mapping (SF-01 → SF-10)
- Immediate termination on structural failure

---

## 2. Semantic Evaluation Engine (`semantic.py`)

Responsible for constraint evaluation.

### Properties
- Sequential evaluation only
- No parallel execution
- No inference
- No skipping
- First-failure selection logic
- Immutable context evaluation

---

## 3. Resolution Engine (`resolution.py`)

Produces final outcome classification.

### Output Types
- **Accepted + Allowed**
- **Accepted + Refused**
- **Rejected (Structural)**

Exactly one classification is always produced.

---

## 4. Validator Controller (`validator.py`)

Controls execution flow.

### Responsibilities
- Phase orchestration
- Phase order enforcement
- Structural → Semantic → Resolution flow
- Prevents phase skipping

---

# 🔄 Phase Flow


The validator executes in strict order:

## Phase Rules

- Structural failure terminates immediately
- Semantic evaluation runs only if structure is valid
- Resolution always produces one final classification
- No optional execution paths exist

---

# ⚡ How Determinism Is Enforced

The validator guarantees deterministic behavior through:

- Frozen grammar definition
- Canonical primitive ordering
- Sequential constraint evaluation
- First-failure selection logic
- Immutable input processing
- No randomness
- No external dependencies
- No global state
- Phase order enforcement
- Cross-instance consistency verification
- Repeat-run determinism testing (1000-run harness)

The same input always produces identical output.

---

# 🚫 Structural Failure Taxonomy

Structural validation errors are mapped to explicit failure classes.

| Code | Failure Type | Description |
|---|---|---|
| SF-01 | Missing Primitive | Required primitive not present |
| SF-02 | Empty ConstraintSet | Constraints list is empty |
| SF-03 | Reason Rule Violation | Missing or forbidden reason |
| SF-04 | Canonical Order Violation | Primitive order incorrect |
| SF-05 | Duplicate Primitive | Duplicate keys detected |
| SF-06 | Multiple Reasons | More than one refusal reason |
| SF-07 | Invalid Outcome | Outcome outside allowed domain |
| SF-08 | Structural Corruption | Invalid primitive or constraint structure |
| SF-09 | ConstraintSet Type Violation | Constraints not a list |
| SF-10 | Primitive Nesting | Primitive embedded inside another |

Structural failures terminate validation immediately.

---

# 🛡 Drift Resistance

The validator prevents:

- Constraint reordering drift
- Outcome manipulation
- Multiple refusal reasons
- Missing refusal reasons
- Allowed outcomes with failing constraints
- Structural corruption attempts

Drift injection tests validate resistance.

---

# 🔒 Determinism Guarantees

The system guarantees:

- Identical output for identical input
- No mutation of context
- No hidden state
- No timing-based variation
- Cross-process consistency
- Repeat-run stability

Determinism is verified using:

- 1000-run repeat harness
- Cross-validator consistency testing
- Constraint isolation validation

---





