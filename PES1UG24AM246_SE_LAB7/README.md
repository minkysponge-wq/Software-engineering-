# Lab 7: Fuzz Testing with Hypothesis — Ski Resort Pass

**Name:** Sampreeth Jaladi · **SRN:** PES1UG24AM246 · **Section:** E
**Assigned repo:** `L6_L7_08_ski_resort_pass`

## About the program

`processor.py` has three input-parsing functions:

- `parse_season_pass_validity("YYYY/MM/DD")` — reports whether a season pass is VALID (year ≥ 2026) or EXPIRED
- `compute_trail_gradient("drop:distance")` — returns the trail slope as a percentage
- `calculate_lift_access_tier("BEG" | "INT" | "ADV" | "ALL")` — returns the lift pass price

## Results

| Run | Result |
|-----|--------|
| `test_processor.py` on the original code | **3 failed, 1 passed** (Hypothesis found 9 distinct crashes) |
| `test_processor.py` on the fixed code | **4 passed** |

Bugs found by fuzzing:

| Function | Failing input | Exception |
|----------|---------------|-----------|
| `parse_season_pass_validity` | `None` | AttributeError |
| | `''` | ValueError |
| `compute_trail_gradient` | `None` | AttributeError |
| | `''` | ValueError (unpack) |
| | `':'`, `'0:'` | ValueError (float) |
| | `'0:0'` | ZeroDivisionError |
| `calculate_lift_access_tier` | `None` | AttributeError |
| | `''` | KeyError |

Fixes: type checks for non-string input, exact part-count checks, `try/except` around `int()`/`float()`, real calendar-date validation, rejection of NaN/inf and zero/negative distance, and `dict.get()` for unknown zone codes. Invalid input now returns an error message (dates) or `None` (gradient, zone) instead of crashing; valid input gives the same results as before.

## Folder structure

```
PES1UG24AM246_SE_LAB7/
├── processor.py            # fixed application
├── processor_buggy.py      # original buggy starter code (for reference)
├── test_processor.py       # completed Hypothesis fuzz tests
├── PES1UG24AM246_SE_LAB7.pdf  # lab report with screenshots
└── screenshots/            # terminal output for every step
```

## How to reproduce

```bash
pip install hypothesis pytest

python processor.py
python -m pytest test_processor.py -v
```
