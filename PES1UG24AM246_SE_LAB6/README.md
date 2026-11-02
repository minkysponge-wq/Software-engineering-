# Lab 6: Code and Branch Coverage — Ski Resort Pass

**Name:** Sampreeth Jaladi · **SRN:** PES1UG24AM246 · **Section:** E
**Assigned repo:** `L6_L7_08_ski_resort_pass`

## About the program

`ski_resort_pass.py` prices ski resort passes (season / full day / half day) using age categories, gear rental, lodge lockers and blackout overrides. It also audits chairlift anemometer logs for two consecutive wind gusts above 45 mph.

## Results

| Test file | Tests | Line coverage | Branch coverage |
|-----------|-------|---------------|-----------------|
| `test_ski_resort.py` (starter) | 1 | 47% | 44% |
| `CodeCoverageTest_PES1UG24AM246_ski_resort_pass.py` | 8 | **100%** | 99% (misses `49->27`) |
| `BranchCoverageTest_PES1UG24AM246_ski_resort_pass.py` | 46 | **100%** | **100%** (42/42 branches) |

The code-coverage suite runs every line but never prices a skier *without* gear rental, so the False side of `if gear_rental:` (`49->27`) is never taken. That's the line-vs-branch gap: 100% of lines executed, yet one decision outcome untested. The branch suite closes it and adds boundary tests (ages 11/12 and 64/65, exactly 4 vs 5 rejections, wind speed exactly 45, fee exactly 0).

## Folder structure

```
PES1UG24AM246_SE_LAB6/
├── ski_resort_pass.py                                  # application under test
├── test_ski_resort.py                                  # starter test file
├── CodeCoverageTest_PES1UG24AM246_ski_resort_pass.py   # line coverage tests
├── BranchCoverageTest_PES1UG24AM246_ski_resort_pass.py # branch coverage tests
├── PES1UG24AM246_SE_LAB6.pdf                           # lab report
└── screenshots/                                        # terminal output for every run
```

## How to reproduce

```bash
pip install coverage pytest

# line coverage
coverage run -m pytest CodeCoverageTest_PES1UG24AM246_ski_resort_pass.py
coverage report -m

# branch coverage
coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM246_ski_resort_pass.py
coverage report -m
```
