# delete_cues_with_missing_cue_id

This script will deleted all cues with missing cue_id from all AvWorks on a client's DB.
The script will also generate a reportal-urls.txt file containing all the affected programs as Reportal URLs to
report them to the CRMs.

To make it work just fill the [.env](.env) file with your right values:

```dotenv
MONGO_URI=mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/{}?retryWrites=true&w=majority
MONGO_USER=CHANGEME:CHANGEME
MONGO_DB=CHANGEME
CUSTOM_PREFIX=removed_bad_cues

# To generate the report of affected docs
DOC_TYPE=AvWork
REPORTAL_URL=https://CHANGEME.bmat.com
```