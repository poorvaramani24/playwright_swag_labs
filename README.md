# Playwright + Pytest Automation Framework

Overview
--------
A Playwright-based Python test automation framework using pytest.  
Implements Page Object Model (POM), configurable environments, parallel execution, retries, logging, HTML reporting, Docker support and artifact capture (screenshots/videos).

Architecture
------------
Simple diagram (text):

```
Project Root
├─ config/         # environment config (yaml/json)
├─ core/           # DriverFactory, base_test, shared framework code
├─ pages/          # POM classes
├─ tests/          # test cases and conftest.py (fixtures)
├─ utils/          # logger, helpers, data loaders
├─ reports/        # html reports, screenshots, videos (artifacts)
├─ requirements.txt
├─ Dockerfile
└─ pytest.ini
```


Capabilities
--------------------------------------------
- Config-driven
  - Put env-specific values (base_url, credentials, browser) in config/*.yaml or .env and load in conftest/core.
- Parallel execution
  - pytest-xdist: run `pytest -n auto` for parallel workers.
- Retry
  - pytest-rerunfailures: use `--reruns <N>` or configure in pytest.ini.
- Logging
  - utils/logger.py: structured logs written to file and console. Include test step logs and failure traces.
- HTML report
  - pytest-html plugin: generates reports/reports.html. Use `--html=reports/report.html`.
- Docker
  - Dockerfile provided to run tests in containerized CI environments.
- POM (Page Object Model)
  - pages/ directory holds classes encapsulating page actions and locators.
- Tags
  - Use pytest markers (e.g., `@pytest.mark.smoke`) and configure markers in pytest.ini to run subsets.
- Video
  - Playwright video recording enabled via context options (DriverFactory). Videos saved to reports/videos/.

How to run (local macOS)
------------------------
1. Create venv and install:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   playwright install
   ```

2. Run single tests:
   ```
   pytest tests/test_login.py::test_valid_login -q
   ```

3. Run all tests in parallel and generate HTML:
   ```
   pytest -n auto --html=reports/report.html --self-contained-html --reruns 2
   ```

4. Common flags:
   - `-k <expr>` run tests matching expression
   - `-m smoke` run marker `smoke` tests
   - `--maxfail=1` stop after first failure

Running in Docker
-----------------
Build:
```
docker build -t playwright_swag_labs .
```
Run (mount reports so artifacts survive):
```
docker run --rm -v "$(pwd)/reports":/app/reports playwright_swag_labs
```
Dockerfile already runs `pytest -n auto` by default. Adjust CMD in Dockerfile if needed.

pytest.ini (recommended)
------------------------
Add to root to centralize pytest settings:
```ini
// filepath: /Users/ramanip/playwright_swag_labs/pytest.ini
[pytest]
testpaths = tests
pythonpath = .
addopts = --strict-markers --html=reports/report.html --self-contained-html
markers =
    smoke: smoke tests
    regression: regression tests
```

Key implementation notes
------------------------
- DriverFactory should expose methods to create browser, context and page with options:
  - headless/headed, record_video_dir, viewport, timeout, accept_downloads.
- conftest.py should provide fixtures:
  - `setup` or prefer `page` fixture (if using pytest-playwright).
  - Load config and set base_url; per-test navigation can be done in fixture.
- Save artifacts on failure:
  - In teardown capture page.screenshot(), page.video_path() (if recorded), and console logs.
- Ensure empty `__init__.py` files in packages to avoid import errors.
- If you get ModuleNotFoundError for core/pages: run pytest from repo root or set pythonpath = . in pytest.ini.

Troubleshooting
---------------
- "No module named 'core'": run from project root or add pythonpath to pytest.ini.
- "fixture 'page' not found": install/configure pytest-playwright or provide your own Playwright fixtures.
- If running inside CI/Docker, ensure `playwright install` is executed (Dockerfile does this).

Example commands summary
------------------------
- Local quick run:
  ```
  source .venv/bin/activate
  pip install -r requirements.txt
  playwright install
  pytest -n auto --html=reports/report.html
  ```
- Docker:
  ```
  docker build -t playwright_swag_labs .
  docker run --rm -v "$(pwd)/reports":/app/reports playwright_swag_labs
  ```

License / Notes
---------------
Keep secrets out of config files in git. Use CI secrets or environment variables for credentials.