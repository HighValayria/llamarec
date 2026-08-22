# Problem Formulation

This paper treats recommendation ability as a set of task-conditioned
capabilities rather than a single scalar property of an adapted LLM. The first
interface is preference prediction. Given a user history and a target item, the
model estimates whether the user will like the item. In the experiments this is
implemented as a Y task, where the model is trained and evaluated through a
yes/no preference interface. The target is explicit preference, and the
paper-facing binary metrics are AUC and validation-calibrated F1 when the
calibration protocol is available.

The second interface is next-item selection. Given the same kind of user
history and a candidate set, the model must identify the actual next
interaction. This is implemented as an N task. The N target is the next observed
interaction, not the next liked item. This distinction matters because the
candidate-label objective does not ask whether each candidate is liked in
isolation. It asks which candidate corresponds to the next event under the
observed sequence.

The two interfaces also induce different ranking scores. A Y adapter can rank
candidates by applying the preference interface independently to each candidate
and sorting by P(Yes). An N adapter instead scores candidate labels in the
next-item interface. The paper keeps these scoring routes separate. When a Y
model ranks poorly under a next-item candidate protocol, the result is not
interpreted as a failure to learn preference. It shows that a preference score
does not directly substitute for a next-interaction ranking score.

The multi-task setting combines both interfaces in one adapted model. In the
current evidence package, M1 is the formal unified model. It exposes a binary
preference path and a candidate-label ranking path, allowing the paper to ask
whether one model can retain both capabilities without erasing the advantages
of task-specific specialists.
