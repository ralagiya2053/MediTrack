---
name: model-selection
description: |
  Recommends 2–3 candidate machine learning algorithms for a specific
  prediction task, based on the findings from a prior EDA run. Reads
  `docs/eda-findings.md` and the user's stated target variable, infers
  the task type (regression, binary classification, multi-class,
  anomaly detection, clustering), applies a structured selection
  framework, and writes a full reasoning report to
  `docs/model-selection.md`. Proposes a `ml/train.py` skeleton. Use
  this skill whenever the user says "which model should I use," "what
  algorithm fits this data," "recommend a model for predicting X,"
  "select an ML algorithm," or any request to choose a model after EDA
  has been done — even without the word "model" if the intent is
  choosing an ML approach for a known target. Always requires EDA
  findings to exist first.

  Not for training the model itself — that's a separate step.
---

# Model Selection

You help the user choose 2–3 candidate algorithms for a specific
prediction task. You do not train models. You produce a reasoned
report and a training-script skeleton.

The goal is **honest recommendations grounded in the EDA findings**,
not the "best" model. The user will train all candidates and pick the
winner empirically. Your job is to narrow the field from "every model
ever invented" to "these 3 make sense for this problem."

---

## Inputs You Require

Before doing anything, confirm both inputs exist:

1. **EDA findings** — `docs/eda-findings.md`
   - If missing: stop and say "Run EDA first (eda-methodology skill)
     so I have findings to base recommendations on."
2. **Target variable** — what the user wants to predict
   - If the user didn't name it: ask, one clear question, no menu.
     e.g. "Which column should the model predict?"

Optionally, if a config exists at `ml/config.yaml`, read it — it may
already declare target, task, and metric. If so, use those; don't ask.

---

## Infer the Task Type

From the EDA findings, look at the target column's dtype and
distribution. Infer:

| Target shape in EDA | Task type |
|---|---|
| Numeric, continuous, many values | **Regression** |
| Categorical with 2 values | **Binary classification** |
| Categorical with 3–20 values | **Multi-class classification** |
| Numeric, but semantically ordered bins | Ordinal (treat as regression or multi-class) |
| > 20 unique values but no obvious continuity | Ask the user — probably an ID or free text |
| No target (unsupervised goal) | Anomaly detection or clustering |

State your inferred task type explicitly and ask for confirmation
before proceeding. If the user corrects you, use their answer.

---

## The Selection Framework

Apply these six keys in order. Each one rules out some families.

### Key 1 — Dataset size
Read the shape from EDA findings (rows × columns).

- **< 200 rows** → linear models, shallow trees. No neural nets.
- **200–5,000 rows** → linear models, random forests, gradient boosting
- **5,000–100,000 rows** → all of the above + XGBoost/LightGBM
- **> 100,000 rows** → any of the above, consider neural nets if nonlinear

### Key 2 — Linearity
Check the EDA correlation matrix (numeric features vs. target).

- **Strong linear correlations (|r| > 0.5)** → start with linear models
- **Weak or nonlinear** → tree-based or kernel models
- **Mixed** → try both, compare

### Key 3 — Feature types
From EDA, count numeric vs. categorical features.

- **Mostly numeric** → any model
- **Mostly categorical** → tree-based (native handling) preferred
- **Mixed** → all families work; note encoding strategy needed

### Key 4 — Interpretability
Ask the user once: "Do you need to explain individual predictions?"

- **Yes** → linear, logistic, decision tree, shallow Random Forest
- **No** → gradient boosting, ensembles, deep models

### Key 5 — Class balance
For classification only. Read class distribution from EDA.

- **Imbalanced (< 15% minority)** → logistic with class_weight='balanced',
  or tree ensembles with scale_pos_weight
- **Balanced** → no adjustment needed

### Key 6 — Time dimension
If EDA flagged a date column:

- **Time-series problem** → require time-based splits, add lag features.
  Algorithms: linear regression with lags, gradient boosting with lags,
  or (for long series) ARIMA/Prophet.
- **Not time-series** → random or stratified splits fine.

---

## Output Structure

Produce `docs/model-selection.md` with this exact structure:
