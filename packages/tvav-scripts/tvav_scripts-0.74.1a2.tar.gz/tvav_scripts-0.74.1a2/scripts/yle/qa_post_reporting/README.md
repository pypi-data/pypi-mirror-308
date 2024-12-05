# YLE Post Report Validation Script

---

## Description
This script generates a QA Report for YLE report batch once the files are generated on the 1st and 15th of each month. 
It should be used to validate whether the batch is OK or not.

## How it works
- Loads the configuration from the environment.
    - Provide the `REPORT_DATE`.
    - Provide the `REPORTS_FOLDER`, where validation will take place
- Performs various checks based on YLE rules and provides csv for each rule if the check fails.

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
python qa_post_reporting.py
```

## Verifying the status
To verify whether the tasks ran successfully, do the following:
- Check `REPORTS_FOLDER` folder location to find the `batch_stats.txt`.
- A new report should appear in YLE DB with "YLE-1868-QA" as report_type
