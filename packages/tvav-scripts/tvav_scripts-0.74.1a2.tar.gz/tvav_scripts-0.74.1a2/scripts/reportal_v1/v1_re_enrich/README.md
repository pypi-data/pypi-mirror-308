# v1_re_enrich

We had some issues with single view metadata. With this script you can perform re-enrichment all music works with specified single view id.

More details here https://bmat-music.atlassian.net/browse/TVAV-9531


### How to use
* Overwrite in .env file the following values:
    
    * MONGO_URI - mongo connection string to the database you want to perform the update.
    * SINGLE_VIEW_URL - single view URL
    * FILE_TO_USE - path to the .csv file that contains all single_view ids to be used to update music works metadata


#### Examples of csv
The .csv file you must provide is following this format:
```csv
sv_sr_id
uuid
```

### Run tests

Step 1: install test dependencies
```sh 
pip install -r test-requirements.txt
```

Step 2: execute tests 
```sh 
pytest tests/scripts/reportal_v1/v1_re_enrich/test_v1_re_enrich.py
```
