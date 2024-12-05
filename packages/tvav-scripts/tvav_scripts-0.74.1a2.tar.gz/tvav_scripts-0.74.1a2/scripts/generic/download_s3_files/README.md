# download_s3_files

This script will download files from bazaar-prod S3 bucket using its File id from tv-av-prod DB.

## Instructions

```dotenv
MONGO_URI=mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/{}?retryWrites=true&w=majority
MONGO_TV_AV_PROD_USER=CHANGEME:CHANGEME
# Bazaar
MONGO_BAZAAR_USER=CHANGEME:CHANGEME
S3_BAZAAR_URI=s3://CHANGEME:CHANGEME/cgpZTeCDkzJxXSxQW2vVHjVcS8@bmat-bazaar-prod
# Use JSON list format, each line containing a string
IDS='[

]'
```

- Replace all "CHANGEME" instances with their actual values
- Add the File ids to the `IDS` env var as in a JSON list of string elements.
Example:
```dotenv
IDS='[
"aisdjaasd",
"asdasdaf",
"asdasd"
]'
```
