# remove_programs_from_bazaar_xml_reports

This script takes an `input.csv` file with 2 columns (`yle_numerical_id` and `ajopvm`)
and updates YLE reports existing in bazaar to remove the specified programs.

## How to run?

1. Create a `.env` file with these 2 env variables filled:

```.env
BAZAAR_MONGO_URI=mongodb+srv://changeme:changeme@bmat-tvav-prod.yq6o5.mongodb.net/bazaar-prod?retryWrites=true&w=majority
BAZAAR_STORAGE_URI=s3://changeme:changeme@bmat-bazaar-prod
```

2. Create an `input.csv` file with the 2 columns specified above.

## How does it work?

1. Init setup
    - Read config from env
2. Read `yle_numerical_ids` and `ajopvm` from `input.csv` file
3. Download all reports that match the date filter
4. Find all report files that contain the programs to remove
5. Update report files with the updated program lists (keep old version as backup)
6. Ask user if to revert or upload changes to bazaar
6.1. If user chosed revert --> restore files from bak copies
6.2. If user chosed upload --> upload files to bazaar
