# Model Selection Report: Resting HR Prediction

## 1. Task Definition
- **Target Variable:** `resting_hr`
- **Task Type:** Regression
- **Goal:** Predict a user's resting heart rate based on other vitals and health logs.

## 2. Selection Reasoning
Based on the EDA findings in `docs/eda-findings.md`, the following factors influenced the selection:

| Key | Finding | Decision |
| :--- | :--- | :--- |
| **Dataset Size** | ~412 vitals readings (Small) | Rule out Deep Learning; focus on linear/tree models. |
| **Linearity** | Extreme correlation (>0.99) between Sleep and HR | Include a linear model as a high-confidence baseline. |
| **Feature Types** | Mixed (Numeric vitals + Categorical symptoms) | Include tree-based models for native categorical handling. |
| **Interpretability** | Health context requires "Why?" | Selected models with clear feature importance/coefficients. |
| **Time Dim.** | Strong Lag-1 autocorrelation | Requires time-based splitting and lag feature engineering. |

## 3. Candidate Algorithms

### Candidate 1: Ridge Regression
- **Type:** Linear Model (L2 Regularized)
- **Reasoning:** The EDA highlighted extreme multicollinearity between vitals. Ridge regression is specifically designed to handle redundant features by shrinking coefficients, preventing the model from becoming unstable.
- **Role:** The "Simplicity" baseline.

### Candidate 2: Random Forest Regressor
- **Type:** Bagging Ensemble (Decision Trees)
- **Reasoning:** Robust to outliers and non-linear patterns. It handles the mixed data types (symptoms/vitals) without requiring extensive scaling and is less prone to overfitting on small datasets than a single deep tree.
- **Role:** The "Robustness" candidate.

### Candidate 3: XGBoost Regressor
- **Type:** Boosting Ensemble (Gradient Boosting)
- **Reasoning:** State-of-the-art for tabular data. If there are subtle non-linear interactions between symptom severity and HR that Random Forest misses, XGBoost's iterative optimization will likely find them.
- **Role:** The "Performance" candidate.

## 4. Training Strategy
- **Feature Engineering:** 
  - Create lag features for `resting_hr` (t-1, t-2).
  - One-hot encode `symptom` categories.
  - Use `StandardScaler` for linear models.
- **Validation:** Use a **Time-Series Split** (e.g., 80% chronological train, 20% chronological test).
- **Evaluation Metric:** Mean Absolute Error (MAE) and R² Score.