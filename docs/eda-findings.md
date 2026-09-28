# EDA Findings — MediTrack Health Data

## What I checked
- **Step 1: Structure** - Analyzed tables `users`, `health_logs`, and `vitals`.
- **Step 2: Nulls and Duplicates** - Checked for missing data and repeats.
- **Step 3: Univariate** - Studied distributions of symptoms, severity, and vitals.
- **Step 4: Target** - Skipped (No target specified).
- **Step 5: Time-awareness** - Analyzed trends and autocorrelation of vitals over time.
- **Step 6: Correlations** - Examined relationships between vitals and symptoms.

## What I found

### Data Structure & Quality
- **Dataset Size**: 3 users, 359 health logs, and 412 vitals readings.
- **Missing Data**: Only `health_logs.notes` contains nulls (~58.8%), which is expected for optional notes. All other critical fields are complete.
- **Duplicates**: No fully duplicated rows or ID collisions were found.

### Distributions
- **Symptom Severity**: Mean is 3.49. Data is skewed toward low severity (1-3), meaning most logged symptoms are mild.
- **Symptom Frequency**: Fatigue and Headache are the most frequently logged symptoms, while Fever and Nausea are the least common.
- **Vitals**: All vitals (Sleep, HR, Weight, BP) stay within expected healthy/moderate ranges with natural day-to-day fluctuation.

### Time & Relationships
- **Temporal Patterns**: Sleep hours show a moderate Lag-1 autocorrelation (0.489), suggesting today's sleep is related to yesterday's.
- **High Multicollinearity**: Extreme correlations (> 0.99) were found between:
    - Systolic BP $\leftrightarrow$ Diastolic BP
    - Weight $\leftrightarrow$ Blood Pressure
    - Sleep Hours $\leftrightarrow$ Resting HR
    - *Note: This is likely an artifact of the seed data generation logic.*
- **Symptom-Vital Links**: Symptom severity shows weak correlation with vitals, suggesting that in this dataset, symptom intensity does not strongly trigger a measurable change in resting vitals.

## What it implies for modeling
- **Imputation**: No imputation needed for vitals/severity; optional notes can be ignored or encoded as "No note".
- **Scaling**: Vitals have different scales (e.g., Sleep ~7 vs BP ~120); any distance-based model (KNN, SVM) will require **StandardScaling**.
- **Redundancy**: Weight and both BP metrics are almost perfectly redundant. Only one representative "cardiovascular/weight" feature should be used to avoid multicollinearity in linear models.
- **Split Strategy**: Because the data is a time series, a **time-based split** (e.g., first 80% of dates for training, last 20% for testing) must be used.

## Open questions
- **Inactive Days**: Should days with no logs be treated as "perfect health" (zero severity) or should they be excluded from analysis?
- **Outliers**: Some severity values hit 10. Should these be treated as critical anomalies or just the top end of a normal range?

## Artifacts
- **Scripts**: `ml/eda/step_1..6_*.py`
- **Plots**: `ml/eda/plots/*.png`
- **Correlation Heatmap**: `![Heatmap](../ml/eda/plots/step_6_correlation_heatmap.png)`
- **Severity Dist**: `![Severity](../ml/eda/plots/step_3_severity_hist.png)`
