---
name: eda-methodology
description: |
  Guides exploratory data analysis (EDA) on any dataset — SQLite
  database, CSV, Parquet, Excel, or a connected DB via MCP. Enforces a
  fixed order of operations (structure → nulls → univariate → target →
  time-awareness → correlations → findings) so no critical check is
  skipped, and runs only the steps that apply to the dataset at hand.
  Saves every step's script, every plot, and the final findings to
  permanent files so the analysis is reviewable and reproducible. Use
  this skill whenever the user asks to explore, profile, understand,
  inspect, summarize, analyze, or "do EDA on" a dataset — including
  phrasings like "EDA on vitals," "what's in this dataframe," "profile
  this CSV," "look at the data first," or any request to understand a
  dataset before modeling — even when "EDA" isn't said explicitly, if
  the intent is to understand data before building a model on it.

  Also applies before writing any feature-engineering or model spec,
  since EDA findings determine the Data Contract.
---

# EDA Methodology

You are guiding exploratory data analysis. The goal is to understand a
dataset thoroughly enough that the *next* step — building a model or
writing a feature spec — can be done with confidence and honesty.

EDA is a disciplined sequence, not a data dump. Follow the order below.
Run only the steps that apply to the data at hand. Skip conditional
steps whose preconditions aren't met, and say so explicitly.

---

## Artifacts — Save Everything to Disk

Every run of this skill produces permanent artifacts. Do not work
purely in memory or print-only.

**Before starting, confirm or create these paths (project root):**
ml/eda/ ← step scripts
ml/eda/plots/ ← all plots
docs/ ← findings summary


**During the run:**

- Save each step's script to `ml/eda/step_N_<short_name>.py`
  - e.g. `ml/eda/step_1_structure.py`, `ml/eda/step_2_nulls.py`
- Save every plot to `ml/eda/plots/` with a descriptive filename
  - Use **PNG** (lossless; JPG blurs chart lines and text)
  - e.g. `ml/eda/plots/step_3_sleep_hist.png`
- Prefix filenames with the step number so they sort naturally

**At the end:**

- Write the full findings report to `docs/eda-findings.md`
  - Include tables, observations, and inline image references to the
    plots using relative paths:
    `![Sleep distribution](../ml/eda/plots/step_3_sleep_hist.png)`
- Optionally propose a `ml/features.py` skeleton based on the findings
  (only if the user asked for it, or if the run was explicitly
  oriented toward modeling)

**Do not skip the saves.** If the user didn't specify paths, use the
defaults above. If the user wants different paths, use theirs. Either
way, the run must leave artifacts on disk.

---

## Data Source — Load Uniformly

The skill applies to any of these. Detect the source, load it into a
single pandas DataFrame, then proceed with the methodology. Do not
change the methodology per source — only the loading step.

### SQLite database (`.db`, `.sqlite`, `.sqlite3`)
- If inside a Flask request context: use `get_db()` from
  `database/db.py`
- If standalone (script, CLI): use `sqlite3.connect(<path>)` directly
- List tables first (`SELECT name FROM sqlite_master WHERE
  type='table'`), then load the relevant table(s) into pandas via
  `pd.read_sql_query`
- Preserve `sqlite3.Row` semantics during queries

### CSV (`.csv`)
- `pd.read_csv(<path>)`
- Watch for: delimiter, encoding, header row, thousands separators
- Report any parsing warnings

### Parquet (`.parquet`)
- `pd.read_parquet(<path>)`
- Fast and type-preserving — no special handling needed

### Excel (`.xlsx`, `.xls`)
- `pd.read_excel(<path>, sheet_name=<name or 0>)`
- If multiple sheets, list them and ask which to load (or load all)

### Connected database via MCP
- Use the MCP tool to list tables and query
- Load the result into pandas for the rest of the methodology

**After loading, always report:**
- Source path or identifier
- Number of tables loaded
- Shape of the resulting DataFrame(s)

---

## The EDA Order

Run these in sequence. Each step may raise follow-ups for the next.
**Skip any step whose precondition is not met** and state why.

### Step 1 — Structure: What is this dataset?

Precondition: always applies.

- **Shape**: rows × columns
- **Column names and dtypes**
- **Memory footprint**
- **Head and tail** (first 5 and last 5 rows)
- **Unique identifier columns** — which column(s) identify a row?

Report as a table. No plots yet.

**Save as:** `ml/eda/step_1_structure.py`

### Step 2 — Nulls and duplicates: What's missing or repeated?

Precondition: always applies.

**Nulls, per column:**
- Count and % of nulls
- Pattern: are nulls random, or do they cluster (by another column,
  by date, by user)?
- Likely cause: is a null "no data" or is it "zero"?

Classify each column's missingness:
- **MCAR** — Missing Completely At Random (safe to drop)
- **MAR** — Missing At Random, depends on another feature (impute
  carefully)
- **MNAR** — Missing Not At Random, depends on the value itself
  (dangerous — investigate)

**Special case for health data:** a null symptom is NOT the same as
"no symptom." It may mean the user didn't log that day. Distinguish
"inactive day" from "active day with no symptom."

**Duplicates:**
- Count of fully duplicated rows
- Count of duplicates on identifier columns (if any)
- Decide: are these legitimate repeats or data errors?

**Save as:** `ml/eda/step_2_nulls_duplicates.py`

### Step 3 — Univariate: One column at a time

Precondition: always applies.

**For each numeric column:**
- Min, max, mean, median, std
- Quartiles (25%, 50%, 75%)
- Histogram / KDE plot
- Outliers: report counts beyond **both** 1.5×IQR and 3σ

**For each categorical column:**
- Value counts
- Cardinality (how many distinct values?)
- Rare categories (values appearing < 5 times)
- Flag high-cardinality (>50 categories) — encoding decision needed

**Plots (save all to `ml/eda/plots/`):**
- Numeric: histogram and boxplot per column
- Categorical: countplot per column

**Save as:** `ml/eda/step_3_univariate.py`

### Step 4 — Target: What are we predicting?

Precondition: a target column has been identified or inferred.
If no target exists, state so and skip.

- **Class balance** (classification) — % per class. Flag if any class
  < 15%.
- **Target distribution** (regression) — histogram, skewness, kurtosis
- **Feature-target relationship** — for each feature, does its
  distribution differ by target value?
  - Numeric feature vs. categorical target: boxplot or distplot
  - Numeric feature vs. numeric target: scatterplot or lineplot
  - Categorical feature vs. categorical target: heatmap of
    contingency, chi-square test
- **Leakage check** — any feature with |correlation| > 0.9 to the
  target is suspicious. Investigate before trusting it.

**Plots:**
- Target histogram (regression) or bar chart (classification)
- Feature-target plots per feature (boxplot / scatter / heatmap)

**Save as:** `ml/eda/step_4_target.py`

### Step 5 — Time-awareness: Only if a date or timestamp exists

Precondition: dataset contains a date or timestamp column.

- **Sort by time** and confirm ordering is correct
- **Autocorrelation** — does today's value predict tomorrow's? Plot
  lag-1, lag-7 correlation
- **Trend and seasonality** — is there a long-term drift? Weekly or
  monthly cycles?
- **Split strategy** — for time-series, ALWAYS use time-based splits,
  never random. State the split boundaries explicitly.
- **Effective sample size** — after removing inactive days or gaps,
  how many usable rows remain?

**Plots:**
- Line plot of each numeric feature over time
- Autocorrelation plot (ACF/PACF) for the target

**Save as:** `ml/eda/step_5_time.py`

### Step 6 — Correlations: Relationships between features

Precondition: at least two columns, at least one pair numeric or
categorical.

Run only after Steps 1–5. Correlation without univariate context is
meaningless.

- **Numeric-to-numeric**: Pearson (linear) and Spearman (monotonic)
  correlation matrix
- **Categorical-to-numeric**: ANOVA F-statistic or Kruskal-Wallis
- **Categorical-to-categorical**: Chi-square test
- **Flag**: any pair with |correlation| > 0.85 is a multicollinearity
  concern

**Plots:**
- Correlation heatmap (numeric)
- Clustermap (categorical)
- Pairplot (all numeric, if column count ≤ 8)

**Save as:** `ml/eda/step_6_correlations.py`

### Step 7 — Findings: What did we learn?

Always run. Produce the structured summary and write it to
`docs/eda-findings.md`.

Format:

EDA Findings — <dataset name>
What I checked
[Bullet list of steps run, and steps skipped with reason]

What I found
[Key facts: shape, nulls, distributions, target balance,
autocorrelation, outliers, notable correlations, cardinality concerns]

What it implies for modeling
[Concrete implications:

Which features need imputation and how

Which features need scaling

Which features are redundant (high correlation)

Which split strategy to use

Expected baseline performance

Any feature that looked like leakage

Any feature dropped due to cardinality or sparsity]

Open questions
[Things that need a decision before proceeding:

Should inactive days be dropped or filled?

Should outliers be clipped or kept?

Is the target definition stable over time?

How to encode high-cardinality categoricals]

Embed plot references inline using relative paths.

**Save as:** `docs/eda-findings.md`

---

## Plot Menu — Choose What Applies

These are the plot types the skill may produce. Do not generate all of
them; generate only what each step requires for the columns that exist.

| Plot | Used for | Step |
|---|---|---|
| Histogram / distplot | Numeric univariate | 3 |
| Boxplot | Numeric univariate + numeric vs. categorical | 3, 4 |
| Countplot | Categorical univariate | 3 |
| Pie chart | Categorical univariate (low cardinality only) | 3 |
| Scatterplot | Numeric vs. numeric | 4, 6 |
| Barplot | Numeric vs. categorical | 4 |
| Lineplot | Numeric over time | 5 |
| Heatmap | Categorical vs. categorical, correlation matrix | 4, 6 |
| Clustermap | Categorical vs. categorical | 6 |
| Pairplot | All numeric columns (≤ 8 columns) | 6 |
| ACF / PACF | Time-series autocorrelation | 5 |

Only generate a pie chart if cardinality ≤ 5. Only generate a pairplot
if numeric column count ≤ 8.

---

## Rules

### Order matters
Never run correlations before univariate. Never run modeling before EDA
is complete. Each step informs the next.

### Conditional execution
Skip steps whose preconditions aren't met, and say so in the findings.
Examples:
- No target column → skip Step 4
- No date column → skip Step 5
- No categorical columns → skip categorical plots

### Distinguish "missing" from "zero"
In health data especially, a null vitals reading is "didn't log."
A null symptom is "didn't log." These are not zeros.

### Never random-split time-series
If the data has a date column, random splits leak future information
into training. Always split by time.

### Check class imbalance before any classification
If the target is imbalanced (< 15% minority), accuracy is misleading.
Report AUC or F1.

### Flag leakage explicitly
If any feature correlates with the target above 0.9, stop and
investigate. It's usually leakage, not signal.

### Report outliers both ways
Report both counts — beyond 1.5×IQR and beyond 3σ. Some fields
(vitals especially) have legitimate outliers.

### Honest reporting
If the dataset is too small for meaningful ML (< 30 rows per target
class), say so. Don't proceed to modeling on a dataset that can't
support it.

### Domain guardrails (for MediTrack and similar health data)
EDA observations must not diagnose, reassure, or alarm. Report facts:

- Safe: "Resting HR ranges from 62 to 84 bpm, mean 71.2."
- Unsafe: "Resting HR is elevated, suggesting cardiovascular strain."

The second crosses into medical interpretation. The app doesn't
diagnose. Neither does its EDA.

### Save everything
Scripts, plots, and findings must persist to disk. A run that leaves
no artifacts is incomplete.

---

## Save Paths — Defaults

Unless the user specifies otherwise:

| Artifact | Path |
|---|---|
| Step scripts | `ml/eda/step_N_<name>.py` |
| Plots | `ml/eda/plots/step_N_<name>.png` |
| Findings | `docs/eda-findings.md` |

Create directories if they don't exist.

Do not commit `meditrack.db` or any real-user data to Git. EDA
artifacts on demo/seed data may be committed; artifacts on real user
data must be gitignored.

---

## Output — What to Show in Chat

For each step, show a short summary in chat:

Step N — <name>
[2–5 bullets of what was found]
Saved: ml/eda/step_N_<name>.py
Plot(s): ml/eda/plots/step_N_<name>.png


Do not print raw code output unless it's short. Summarize into tables.
The full detail lives in the saved files.

At the end, present the findings summary and confirm all artifacts
were saved.

---

## Example — First Exchange on a MediTrack Dataset

**User:** "Do EDA on the vitals data."

**You:**

> I'll walk through the EDA order and save everything to disk.
>
> One assumption first: since MediTrack stores vitals in long format
> (one row per metric per reading), I'll pivot to one row per user per
> day before Steps 3+. If you'd prefer EDA on the raw long table, say
> so.
>
> Starting with **structure**.
>
> Saved: `ml/eda/step_1_structure.py`
> Shape: 87 rows × 5 columns (after pivot: 87 × 8)

Then proceed through each step, saving artifacts as you go. Pause at
any surprise and ask whether to investigate before continuing.

At the end:

> All artifacts saved:
> - Scripts: `ml/eda/step_1..7_*.py`
> - Plots: `ml/eda/plots/*.png`
> - Findings: `docs/eda-findings.md`
>
> Open questions for the feature builder:
> [list from Step 7]

---

## When to Stop and Ask

Pause the run and ask the user if:

- The dataset has multiple tables and it's unclear which to analyze
- A target column can't be inferred and none was named
- A "column" is actually an ID (drop before analysis, or keep?)
- The dataset has more than 8 numeric columns (pairplot won't scale)
- Any finding looks like leakage (correlation > 0.9 to target)

Do not power through these. Each one changes the analysis.