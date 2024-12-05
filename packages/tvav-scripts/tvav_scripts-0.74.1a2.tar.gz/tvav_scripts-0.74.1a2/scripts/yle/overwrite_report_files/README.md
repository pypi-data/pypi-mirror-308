# overwrite_report_files

This script uploads to bazaar all files inside a sub-directory.

It uses yle-reports-fortnightly with the same name of the file to overwrite the already existing file.

## How to run?

1. Create a `.env` file with these 3 env variables filled:

```.env
BAZAAR_MONGO_URI=mongodb+srv://changeme:changeme@bmat-tvav-prod.yq6o5.mongodb.net/bazaar-prod?retryWrites=true&w=majority
BAZAAR_STORAGE_URI=s3://changeme:changeme@bmat-bazaar-prod
REPORTS_DIR_TO_USE=""
```

2. Run the script
