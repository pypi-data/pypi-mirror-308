# report_files_received_from_log

This script can be used to find and report files received by any client, as long as they can
provide us with the IDs of the files ingested.

Reads **INPUT_FILENAME** text file and searches for File documents in **tv-av-prod / file**.

Generates 3 reports:
- output.csv: report with all found File documents.
- not_found.csv: report with all File documents not found in DB.
- meta.csv: report with info requested in the ticket:
    - Number of files in **INPUT_FILENAME**.
    - Number of files in DB.
    - Duplicated count (unique File ID + number of appearances in **INPUT_FILENAME**).

## Instructions

Just rename [.env.template](.env.template) as **.env** and fill it in with
your needed values.

> **INPUT_FILENAME** must be a text file containing 1 File ID per line.

```dotenv
MONGO_CREDENTIALS="CHANGEME:CHANGEME"  # User with read permissions on tv-av-prod
INPUT_FILENAME="CHANGEME"  # The file with File ids to look for.
```