# Check Epg Sync Script

## Description
This script will try to generate an Epg Sync Package with all programs
within `START_TIME` and `END_TIME` that also have "No epg sync"
as `error_description` (for ALL CHANNELS / selected channel by its
`CHANNEL_DISPLAY_NAME`). 

## How it works
- Loads the configuration from the environment
- If `ONLY_NO_EPG_SYNC` is `True`
    - Fetches all programs within specified date range with "No epg sync" as error description
- Else:
    - Fetches all programs within specified date
- Fetches the channel / all channels
- Calls the method `create_work_package` from `epg_processor_bundle`

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
python v1_reimport_index.py
```

## Verifying the status
To verify whether the tasks ran successfully, do the following:
- Check last epg packages in EpgSyncTool with the `generic_annotator` user.
