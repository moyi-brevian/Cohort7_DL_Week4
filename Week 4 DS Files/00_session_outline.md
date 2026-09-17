# Data Mondays — Week 4 Class Session (2 hours)
## Descriptive Stats, Visualisation, Data Quality & APIs — Amani Insurance Case Study

**Format:** Same as Week 2 — no live coding. All code is pre-written and
commented; you present/walk through it, pause for discussion, and run it
live to show output.

**Domain:** Amani Insurance (fictional), a Kenyan motor/health/property
insurer. Claims are hand-logged by assessors across six regional offices
(Nairobi, Mombasa, Kisumu, Eldoret, Nakuru, Nyeri) — same "realistic,
messy operational data" hook as Week 2's KPC case study, now applied to
stats, visualisation, and data quality instead of pure syntax.

## Files used in this session

| File | Purpose |
|---|---|
| `insurance_claims_messy.csv` | Main dataset — hand-logged claims, deliberately messy |
| `policyholders.json` | Policyholder master data (system-exported, cleaner but not perfect) |
| `exchange_rates_cache.json` | Offline fallback for the live API demo |
| `generate_messy_data.py` | (Tutor only) reproducibly regenerates all three data files |
| `01_descriptive_stats.py` | Part 1 walkthrough |
| `02_visualisation.py` | Part 2 walkthrough (saves PNGs to `plots/`) |
| `03_missing_outliers.py` | Part 3 walkthrough |
| `04_numpy_operations.py` | Part 4 walkthrough |
| `05_apis_and_files.py` | Part 5 walkthrough (needs `requests`; falls back offline automatically) |
| `06_student_exercise.py` | In-class/take-home exercise with TODOs covering all five deliverables |

## 0:00 – 0:10 | Welcome & Week 4 roadmap (10 min)
- Recap: Weeks 1–3 built the muscle for working with data structures,
  functions, classes (and by now, presumably pandas). This week is about
  turning cleaned data into **numbers and pictures a decision-maker can
  act on** — plus getting data INTO Python from more places (APIs, JSON).
- Introduce Amani Insurance: five... six regions, claims logged daily by
  assessors, a policyholder master file exported from a separate system.
- Show `insurance_claims_messy.csv` for 60 seconds — same "this is what
  real data looks like" hook as Week 2, now with insurance-specific
  messiness: missing claim amounts, a few negative amounts (sign-entry
  errors), some suspiciously huge claims (typos or genuine large losses —
  which is which?).
- State the thread for today: **stats → visualise → clean (missing/
  outliers) → NumPy speed → bring in outside data (API/JSON)**.

## 0:10 – 0:30 | Part 1 — Descriptive Statistics (20 min)
Run `01_descriptive_stats.py` section by section.
- Section 1–2: load the CSV, do the *minimum* cleaning needed to make
  `claim_amount_kes` numeric (full cleanup is deliberately deferred to
  Part 3 — don't get pulled into a tangent here).
- Section 3: mean vs median vs mode vs std, and why mean > median here
  signals a right-skewed distribution — a classic insurance pattern.
- Section 4: same four numbers broken down by claim type via
  `groupby().agg()`.
- Use the discussion prompts at the bottom of the file.

## 0:30 – 0:55 | Part 2 — Visualising Distributions (25 min)
Run `02_visualisation.py`.
- Section 1–2: a Matplotlib histogram, then the same one log-scaled —
  ask students to predict the shape from Part 1's numbers *before*
  revealing the chart.
- Section 3: Seaborn `histplot` with `hue=claim_type_clean` — same idea,
  far less code than the Matplotlib equivalent.
- Section 4: Seaborn boxplot, log-scaled — this is the visual preview of
  the IQR outlier method coming in Part 3.
- Section 5: countplots for categorical columns (region, status) —
  different question ("how many of each category") than a histogram.
- All plots also save to `plots/` as PNGs if you want them for slides.

**5–10 min break here if your 2 hours allows it, or fold into transition.**

## 0:55 – 1:20 | Part 3 — Missing Values & Outliers (25 min)
Run `03_missing_outliers.py`.
- Section 1–2: quantify missingness, then walk through THREE strategies
  (drop / fill with overall median / fill with per-group median) and why
  the per-claim-type median is the right call here specifically.
- Section 3–4: the IQR method for flagging outliers, done PER claim type
  (not globally) — and the important distinction between a *statistical*
  outlier (flag, investigate) and an *unambiguous data error* (negative
  amount — just fix it).
- Section 5: `clean_claims()` — the reusable pipeline function everything
  else in the course can now build on.

## 1:20 – 1:45 | Part 4 — NumPy for Efficient Numerical Work (25 min)
Run `04_numpy_operations.py`.
- Section 1: a live, timed loop-vs-vectorised comparison — the actual
  speedup number will vary by machine, that's fine, the point is the gap
  is real and grows with data size.
- Section 2: boolean masking to reveal the classic "80/20" insurance
  pattern (small share of claims by count = most of the value).
- Section 3: `np.where` for vectorised if/else, building risk bands.
- Section 4: reshaping into a region-by-month matrix and aggregating
  with `axis=0` vs `axis=1` — worth slowing down on, this trips
  everyone up at least once.

## 1:45 – 1:55 | Part 5 — APIs, CSV & JSON (10 min, can extend if time allows)
Run `05_apis_and_files.py`.
- Section 1: loading the same CSV as always, plus a NEW source —
  `policyholders.json` — two ways (`json.load` vs `pd.read_json`).
- Section 2: fetching a live USD/KES exchange rate from a free, keyless
  API, with an automatic offline fallback to a cached JSON file if the
  room's wifi misbehaves — **if the fallback triggers live in class,
  that's the demo working as designed, not something broken.**
- Section 3: joining claims + policyholders + exchange rate into one
  view, reporting reinsurance-ceded claims in both KES and USD.
- If time is short, Section 1 and the fallback explanation can be
  compressed to "here's the idea" — the take-home exercise reinforces it.

## 1:55 – 2:00 | Wrap-up (5 min)
- Recap the thread: raw numbers → stats → pictures → trustworthy data →
  fast numeric ops → data from anywhere. This is the shape of a real
  analytics workflow, insurance or otherwise.
- Assign `06_student_exercise.py` as homework/practice — it has one TODO
  per deliverable, each pointing back to the exact section of today's
  walkthrough that shows the pattern to copy.

## Instructor notes / anticipated questions
- **"Why did some sections only do 'light' cleaning instead of full
  cleanup?"** — Deliberate: Part 1 and Part 2 do just enough cleaning to
  make the numbers/charts meaningful, so the FULL missing-value/outlier
  treatment in Part 3 lands as its own clear topic instead of being
  smeared across every file. `clean_claims()` in Part 3 is the one true
  cleaned version everything downstream should build on.
- **"The API call failed during my demo!"** — By design, `05_apis_and_files.py`
  never crashes on that; it falls back to a cached rate automatically. Use
  it as a live teaching moment about why production code always needs a
  fallback path, not a sign something's broken.
- **"Why insurance and not something more familiar to students?"** —
  Same rationale as Week 2's KPC choice: claims data has real
  right-skewed distributions, real missing/outlier problems, and a
  natural reason to reach outside the CSV (an exchange-rate API) — every
  Python concept this week earns its place instead of feeling arbitrary.
