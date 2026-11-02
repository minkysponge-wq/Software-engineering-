# Lab 5 — Issue Table (maintenance_system.py)

Sampreeth Jaladi · PES1UG24AM246 · Line numbers refer to the original starter file.

| # | Issue | Tool / Code | Severity | Type | Line(s) | Description | Fix Approach |
|---|-------|-------------|----------|------|---------|-------------|--------------|
| 1 | Insecure temp file | Bandit B306 (CWE-377) | Medium | Security | 40 | `tempfile.mktemp()` returns a name only; another process can create that path first (race, symlink attack) | `tempfile.NamedTemporaryFile(..., delete=False)` creates and opens the file atomically |
| 2 | `assert` used for runtime check | Bandit B101 (CWE-703) | Low | Security / Bug | 61 | Asserts are stripped under `python -O`, so the "no assets" guard disappears | Replaced with an explicit `if not assets:` check that prints a message and returns |
| 3 | Mutable default argument | Pylint W0102 | Medium | Bug | 10 | `logs=[]` is created once and shared across every call | Default to `None`; fall back to an explicit module-level `registration_log` |
| 4 | Bare `except` | Pylint W0702 / Flake8 E722 | Medium | Bug | 18 | Swallows every exception, including `KeyboardInterrupt` and typos | Catch only `KeyError` (unknown asset); date errors caught separately as `ValueError` |
| 5 | `open()` without `with` / encoding | Pylint R1732, W1514 | Medium | Bug / Resource | 34, 41 | File handle leaks if `write()` raises; output encoding depends on platform | `with open(..., encoding="utf-8")` and `json.dump()` |
| 6 | `global` statement | Pylint W0603 | Medium | Design | 30 | Mutating a module constant via `global` hides state changes | Interval moved into a `settings` dict; `SERVICE_INTERVAL_DAYS` constant removed |
| 7 | Unused import | Pylint W0611 / Flake8 F401 | Low | Style | 2 | `logging` imported but never used | Removed |
| 8 | Non-snake_case name | Pylint C0103 | Low | Style | 46 | `printAlerts` violates PEP 8 naming | Renamed to `print_alerts` |
| 9 | Iterating dict keys then indexing | Pylint C0206 | Low | Style | 23 | `for a in assets: assets[a]...` | `for asset_id, info in assets.items()` |
| 10 | Missing docstrings | Pylint C0114, C0116 | Low | Docs | 1, all functions | No module or function docstrings | Added module and function docstrings |
| 11 | Blank lines / line length | Flake8 E302, E305, E501 | Low | Style | 10–66 | One blank line between functions; line 11 is 98 chars | Two blank lines between definitions; wrapped the dict literal |
| 12 | Module runs on import | Manual | Low | Design | 66 | Bare `main()` runs whenever the file is imported | `if __name__ == "__main__":` guard |

## Logic bugs found by running the program (no tool flags these)

| # | Issue | Line(s) | Observed behaviour | Fix Approach |
|---|-------|---------|--------------------|--------------|
| 13 | Empty asset ID accepted | 53 | `Registered  - ...` and an alert for asset `""` | Reject empty/whitespace IDs in `register_asset` |
| 14 | Duplicate ID silently overwrites | 54 | FL-01 Forklift became "Crane" and its service date reset | Reject IDs that are already registered |
| 15 | Negative interval accepted | 57 | `change_interval(-30)` made every asset overdue, including ones serviced today | Accept only positive integers; keep the previous value otherwise |
| 16 | User date not validated | 58–60 | Input like `bad` is stored, then `strptime` crashes in `due_for_inspection` with `ValueError` | Parse with `strptime` on input; reject invalid formats and future dates |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.55/10 (19 messages) | **10.00/10** |
| Bandit | 2 issues (1 Medium, 1 Low) | **0** |
| Flake8 | 12 violations | **0** |
