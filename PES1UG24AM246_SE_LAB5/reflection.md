# Lab 5 — Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the mechanical style issues: Flake8's blank-line rules (E302/E305), the unused `logging` import, renaming `printAlerts` to `print_alerts`, and adding docstrings. Each one has a single obvious fix that doesn't change behaviour. The hardest were the issues that needed a design decision. Removing the `global` statement meant choosing where the interval should live; I used a `settings` dict. Fixing the mutable default `logs=[]` was harder than it looks: switching to `None` alone would have changed the "total registrations this run" output, so the shared state had to become explicit as `registration_log`. The logic bugs (empty IDs, duplicate overwrite, negative interval, unvalidated dates) were hardest of all, because no tool flagged them and I only found them by running the program and reading the output.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

None were wrong, but some were low value in context. Bandit's B101 (`assert_used`) is a generic rule: in a test file, `assert` is correct and B101 is a false positive. Here it was a real issue, because the assert was a runtime guard that disappears under `python -O`. Pylint's C0116 docstring warnings are also arguably noise for small, self-explanatory functions. Going the other way, there were false negatives: all three tools passed code that registered an empty ID, overwrote an existing asset, and accepted a negative service interval. A clean report doesn't mean correct code.

**3. How would you integrate static analysis tools into your actual software development workflow?**

- **Locally:** run Flake8 and Pylint on save in the editor, plus a `pre-commit` hook running `flake8`, `pylint --fail-under=9.5` and `bandit -r .`, so issues are caught before a commit exists.
- **CI:** a GitHub Actions job on every push and pull request that runs all three tools and fails the build on any Bandit Medium/High finding, any Flake8 error, or a Pylint score under the threshold. Reports are uploaded as build artifacts.
- **Configuration:** keep rules in `pyproject.toml` / `.flake8`, so the team shares one standard and intentional exceptions are documented (e.g. `# nosec` with a reason) rather than silently ignored.

**4. What tangible improvements did you observe in code quality, readability, or robustness after applying the fixes?**

- **Scores:** Pylint went from 6.55 to 10.00/10, Bandit from 2 issues to 0, Flake8 from 12 violations to 0.
- **Security:** the scratch file is now created atomically with `NamedTemporaryFile`, closing the `mktemp` race condition.
- **Robustness:** files are closed even on error (`with`) and use explicit UTF-8. Only `KeyError` and `ValueError` are caught, so real bugs aren't hidden. An invalid date input no longer crashes the program.
- **Correctness:** the program now rejects empty IDs, duplicate registrations, non-positive intervals, and malformed or future dates. Before, it silently produced wrong alerts.
- **Readability:** PEP 8 naming and spacing, docstrings, `.items()` iteration, no `global`, and a `__main__` guard, so the module can be imported and tested without side effects.
