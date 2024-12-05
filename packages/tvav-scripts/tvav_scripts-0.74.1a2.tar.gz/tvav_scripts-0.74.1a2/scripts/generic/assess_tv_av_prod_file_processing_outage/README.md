# `assess_tv_av_prod_file_processing_outage`

This script can be used to assess outages impact on Reportal.

After running this script a new `reports` directory will be created at the same level as the script,
with the following report files:

- `cued_to_re_process.csv`: file ids to be used to re-process files (CUED)
- `cued_to_import.csv`: file ids to be used to re-import files (CUED)
- `reportal_to_process.csv`: file ids to be used to re-process files (REPORTAL)
- `error.csv`: file ids for files with error status
- `unexpected_please_review_manually.csv`: file ids of statuses not expected by the script, please check manually each one
- `bazaar_prod_files_missing_in_tv_av_prod.csv`: bazaar files that were not found in tv-av-prod (searched using namespace and name)

## How to run?

Copy the .env.template file to .env and fill the env variables to your use case.
