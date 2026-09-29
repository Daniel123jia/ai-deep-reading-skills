# Critical Analysis and Follow-up Rules

Use these rules for section 05 and section 06.

## Core weakness test
A core weakness should threaten at least one of: mechanism validity, causal interpretation, generalization, evaluation fairness, scalability/efficiency, or reproducibility of a central claim. Prefer 2–4 high-value weaknesses.

For each weakness: Weakness → Why it matters → Potential impact → Suggested validation → Evidence.

Do not inflate the list with generic complaints such as “more datasets would be useful” unless dataset breadth is essential to a universal claim.

## From assumptions to weaknesses
High-risk assumptions are good candidates for core weaknesses when their failure would undermine a core claim. Link them with `related_assumption_ids`.

## From weaknesses to open questions
Convert a weakness into an open question only when the uncertainty is scientifically meaningful and testable. State why it matters and how to validate it.

## From open questions to research directions
A research direction should name the problem to investigate, not invent the solution. Good: “reliability-aware local matching under background clutter”. Too far: “propose X-Net with three attention modules”.
