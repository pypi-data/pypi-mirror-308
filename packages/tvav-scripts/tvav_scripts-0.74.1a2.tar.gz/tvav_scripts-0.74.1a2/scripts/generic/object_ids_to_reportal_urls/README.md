# object_ids_to_reportal_urls

This script can be used to generate reportal links from a collection of ObjectIds.
Useful to report links of affected programs or cuesheets to the CRMs.

In order to use the script, please fill the [.env](.env) file with the right values
(reportal base url of client's app and the type of document for the ObjectIds).

```dotenv
#DOC_TYPE=AvWork
DOC_TYPE=Schedule
REPORTAL_URL=https://nrk-stg-reportal.bmat.com
```

Then add the ObjectIds you want to convert to reportal links in the [object_ids.txt](object_ids.txt) file
and run the script. When it finishes a new file will be created with the urls called `reportal_urls.txt`
at the root of this script.

As an example, the object_ids.txt file can take as input the following patterns:
```
ObjectId("63d9c7cd6b094702866c5dd6")
63d9c8437e23f1d63a6c7d16
ObjectId("63db1953b5eeea9b284b2cc3"),
63db193db5eeea9b284b2c5e,
```

> At the moment, only `Schedule` and `AvWork` are valid `DOC_TYPE` values.
> 
> `DOC_TYPE` is used to determine if the reportal link will be formed using "programs" or "cuesheets"

# Update
Now you can call this function from other scripts to generate a report of your affected docs.