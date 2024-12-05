# re_enrich_music_works

!!!! IMPORTANT !!!!
FOR YLE run the `yle_prepare_re_enrichment.py` script with the summary from the QA pre report, it will generate a `input.csv`
file with every `single_view_id` to be re-enriched and another `yle_pre_enrichment_error.txt` file with every SV URL we
couldn't get the sv_id for from SV API.

---

This script is an adaptation of a snippet script. It is very usefull to reenrich a list of music works if for any reason we have to (for example in the first case it was for a problem with SV).

It is meant to be used for music_work >3, so if the client is V1 or V2 but not upgraded (they will have the populated pod), this will not work.

# How to use

> Personal suggestion: run this script once with DRY_RUN set to True to get an estimation on impact and ETA
> Also, super recommended: run in av-fabric-stg to reduce connection issues.
 
* Overwrite in .env file the following values for the customer:
    
    * REPORTAL_DOMAIN
    * CUSTOM_VALUES
    * MONGODB__CREDS
    * MONGODB__DB_NAME
    * FILE_TO_USE
    * COMMISSIONED_MUSIC_CRAWLER
    * CUSTOM_ID_FIELD
    * CSV_WITH_HEADER
    * SINGLE_VIEW_IDS_STILL_VALID
    * DRY_RUN (If True, won't save to DB, only generate reports)
    * TOTAL_AV_WORKS_AFFECTED_PER_MUSIC_WORK_LIMIT
    * IS_MUSIC_WORKS_IDS (set to True to use MusicWork IDs in the input file)
    * REPLACE_WORK_IDS (if True, will update existing work_ids)
* Overwrite the customer package in the requirements.txt file with your customer package
* Add in the folder `to_reerich` the csv with the single views sound recording ids
* run the script
```bash
python re_enrich_music_works.py 
```
# Examples of csv

The csv you must provide is following this format:

```csv
sv_sr_id
uuid
uuid
uuid
...
```

You can also use a csv without headers, but in that case the env value `CSV_WITH_HEADER` must be `"False"`

# Types of re enrich

If the single view ids are still working remember to set the env value `SINGLE_VIEW_IDS_STILL_VALID` as `"True"`. But,
if the single view ids are not valid, you must set it up to `"False"`

# Affected AVWorks for CRMs

This script will also generate a file with the ids of the affected AvWorks (the ones that has at least 1 match in the 
cuesheet). But, sometimes a MusicWork can be related with thousands of AvWorks, so as we don't want all the matches in 
the file, you can specify how many matches do you want in the file using the env value 
`TOTAL_AV_WORKS_AFFECTED_PER_MUSIC_WORK_LIMIT`. 

But we still will have in the MusicWork file the number of affected AvWorks by the update   
