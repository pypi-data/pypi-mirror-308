# qa_pre_reporting Script

This script was requested for ticket [YLE-1868](https://bmat-music.atlassian.net/browse/YLE-1868).

---

## Description
This script generates a QA Report for YLE report batches without marking any program as
reported. It can be used to prevent issues in real reports.

## How it works
- Loads the configuration from the environment.
    - You can choose the `REPORT_DATE`.
    - You can also point to STG if needed.
- Populates a new stat report and generates the report as an Excel document with
1 sheet per channel in the report.

## Quickstart guide
### Prerequisites
- Python `>=3.9`
- Install all dependencies from `requirements.txt`:
  - `pip install -r requirements.txt`
- To run the tests, also install dependencies from `test-requirements.txt`:
  - `pip install -r test-requirements.txt`
- Make sure to fill all the variables in a `.env` file, the script relies on that.

### Running the script
Run the script:
```shell
python qa_pre_reporting.py
```

## Verifying the status
To verify whether the tasks ran successfully, do the following:
- Check script folder to find the QA report.
- A new report should appear in YLE DB with "YLE-1868-QA" as report_type
