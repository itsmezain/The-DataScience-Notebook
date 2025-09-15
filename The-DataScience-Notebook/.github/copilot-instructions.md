<!-- .github/copilot-instructions.md for The-DataScience-Notebook -->
# Repo summary

This repository is a teaching collection of Jupyter notebooks and small example apps focused on Python data-science topics (NumPy, Pandas, Flask, Streamlit, basic ML). Notebooks live under `Lecture XX ...` folders. Small runnable examples live alongside notebooks (for example `Lecture 26 Flask Web Devlopment/app.py` and `Lecture 31 API Development Using Flask/IPL API service/ipl.py`).

## What an AI coding agent should know up-front

- Purpose: this repo is primarily educational examples and exercises. Changes should preserve notebook content and small demos unless asked to refactor or replace an example.
- Primary file types: `.ipynb` notebooks, small Python scripts (`.py`), CSV datasets, and occasional `requirements.txt` files under lecture subfolders.
- No centralized application or CI is present. Assume manual testing via: `jupyter notebook`, `python <app>.py`, or `streamlit run <script>.py`.

## Directory & pattern highlights (examples)
- Notebooks: `Lecture 1 Python Basic/`, `Lecture 26 Flask Web Devlopment/`, `Lecture 41 Pandas Case Study - Time Series Analysis/` — open the `.ipynb` for intent and narrative before editing.
- Flask demos: `Lecture 26 Flask Web Devlopment/app.py` and small APIs under `Lecture 31 API Development Using Flask/IPL API service/` — these run with `python app.py` and are intentionally minimal (debug mode often used).
- Streamlit demo: `Lecture 36 Streamlit- Indian Startup DashBoard/Indian Startup dashboard using Streamlit/` — run with `streamlit run 1- Streamlit Basic practise.py` (or the provided entry script). Check `requirements.txt` in that folder for needed packages.

## Developer workflows & quick commands
- Run notebooks: start a Jupyter server in the repo root: `jupyter notebook` and open the `.ipynb` file.
- Run a Flask demo: `python "Lecture 26 Flask Web Devlopment/app.py"` (Windows PowerShell — quote paths with spaces).
- Run Streamlit: `streamlit run "Lecture 36 Streamlit- Indian Startup DashBoard/Indian Startup dashboard using Streamlit/1- Streamlit Basic practise.py"`.
- Create a lightweight virtual environment and install dependencies when modifying demos: `python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt` (if a top-level `requirements.txt` exists) or install the lecture-specific requirements file.

## Editing conventions & guardrails for AI edits
- Preserve notebook narrative: when touching `.ipynb` files, prefer edits to code cells only and avoid removing explanatory markdown unless requested.
- Small runnable scripts intentionally use `app.run(debug=True)` and simple prints — avoid changing `debug` behavior unless asked to add a production-ready change.
- Use explicit, minimal diffs: avoid large, sweeping refactors across many lecture folders. Propose changes as separate PRs per lecture/demo.

## Patterns to reference when making code changes
- Data files are often CSVs next to notebooks (e.g., `Lecture 40 .../expense_data.csv`, `Lecture 39 .../time_series_covid19_confirmed_global.csv`). Use relative paths and do not hardcode absolute filesystem locations.
- Example API logic lives in `Lecture 31 API Development Using Flask/IPL API service/ipl.py` — follow its simple function-return-dict style when adding similar utilities.
- Streamlit demos include `requirements.txt` in their subfolder — check those before running.

## What not to do (quick list)
- Don't delete or move notebooks without explicit instruction — these are teaching artifacts.
- Don't assume a test harness or CI; run examples locally when validating behavior.

## If you need more info
- To add bigger features or refactors, run these checks first: open the relevant `.ipynb` to understand the lesson, run the demo locally, and list any new dependency in a `requirements.txt` in that lecture folder.
- If something is ambiguous, ask where the change should live (which lecture folder) and whether the notebook narrative must be updated.

---
Please review and tell me if you want additional rules (for example: a strict pre-commit/test step, or a preferred venv/packaging approach).
