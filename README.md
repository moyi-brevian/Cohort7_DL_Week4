# Cohort7_DL_Week4
 Week 4 practical content.
# Data Mondays — Class Materials

Hands-on Python and data-analysis teaching materials, built around realistic,
deliberately messy case studies rather than toy datasets. Each week pairs a
business scenario with a specific set of skills, so every concept has a
concrete reason to matter.

No live coding in class — code is pre-written, commented, and run live to
show output, with pauses for discussion.

## Weeks included

### Week 2 — Data Manipulation & the Python Toolbox
**Case study:** Kenya Pipeline Company (KPC) depot operations
**Covers:** strings, lists & dictionaries, writing functions, OOP, inheritance
**Folder:** [`week2_kpc/`](./week2_kpc)

### Week 4 — Descriptive Stats, Visualisation, Data Quality & APIs
**Case study:** Amani Insurance motor/health/property claims
**Covers:** descriptive statistics, Matplotlib/Seaborn, missing values &
outliers, NumPy, fetching data from APIs and loading CSV/JSON
**Folder:** [`week4_insurance/`](./week4_insurance)
**Format:** Jupyter notebooks (`.ipynb`)

## Structure

Each week's folder follows the same pattern:

| File | Purpose |
|---|---|
| `00_session_outline.md` | 2-hour timed class roadmap |
| `generate_messy_data.py` | Tutor-only — reproducibly regenerates the dataset(s) |
| `*.csv` / `*.json` | The dataset(s) students work with |
| `01_...` → `0N_...` | Numbered walkthrough scripts/notebooks, one per topic |
| `0N_student_exercise` | In-class/take-home exercise with TODOs |

## Requirements

```bash
pip install pandas numpy matplotlib seaborn requests
```

Week 4 uses Jupyter notebooks:

```bash
pip install jupyter
jupyter notebook week4_insurance/
```

## Usage

1. Clone the repo.
2. `cd` into the week you're teaching.
3. Run `generate_messy_data.py` once if you want to reseed the dataset
   (already-generated CSVs/JSONs are committed, so this is optional).
4. Open the numbered files in order and run them live in class.

## License

Add your preferred license here (e.g. MIT) if this will be shared publicly.
