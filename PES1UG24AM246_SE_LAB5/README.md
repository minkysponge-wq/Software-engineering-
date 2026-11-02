# Lab 5: Static Code Analysis — Warehouse Asset Maintenance Registry

**Name:** Sampreeth Jaladi · **SRN:** PES1UG24AM246 · **Section:** E
**Assigned repo:** `L5_08_warehouse_assets` · **File:** `maintenance_system.py`

## About the program

A maintenance registry for warehouse equipment. It registers machines, records service dates, raises alerts for overdue inspections, and exports a report to `maintenance.json`.

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.55/10 | **10.00/10** |
| Bandit | 2 issues (1 Medium, 1 Low) | **0** |
| Flake8 | 12 violations | **0** |

Besides the tool findings, four logic bugs were found by running the program: an empty asset ID was accepted, a duplicate ID silently overwrote an existing asset, a negative service interval was accepted, and an invalid date input crashed the program. All four are fixed.

## Folder structure

```
PES1UG24AM246_SE_LAB5/
├── maintenance_system.py        # fixed source file
├── issues.md                    # issue table (16 issues)
├── reflection.md                # answers to the reflection questions
├── PES1UG24AM246_SE_LAB5.pdf    # lab report
└── reports/
    ├── before/                  # pylint, bandit, flake8 reports on the original code
    └── after/                   # the same reports after the fixes
```

## Commits

1. Add Lab 5 starter code
2. Add baseline pylint, bandit and flake8 reports (before fixes)
3. **Fix Bandit issues**: insecure `tempfile.mktemp` (B306) and `assert` check (B101)
4. **Fix Pylint issues**: mutable default, bare `except`, `global`, `with`/encoding, naming, docstrings, input validation
5. **Fix Flake8 issues**: PEP 8 blank lines (E302/E305)
6. Add after-fix reports, issue table and reflection
7. Add Lab 5 report

## How to reproduce

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install pylint bandit flake8

python maintenance_system.py

pylint maintenance_system.py > pylint_report.txt
bandit -r maintenance_system.py > bandit_report.txt
flake8 maintenance_system.py > flake8_report.txt
```
