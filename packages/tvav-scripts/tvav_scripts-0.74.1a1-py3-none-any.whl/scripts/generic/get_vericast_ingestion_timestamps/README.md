# get_vericast_ingestion_timestamps

This script is useful for Tickets like [TVAV-9268](https://bmat-music.atlassian.net/browse/TVAV-9269)
which requires a report of Vericast ingestion timestamps.

- Valid input CSV format
```csv
Name;Path_File;File-ID;Upload-Starting-Date;Status;
```
- Output CSV format
```csv
Start_Time_UTC,End_Time_UTC,Input_Name
```
**EXTRA**: If any file is missing its recording info or data field
the error will be appended to the output CSV file surrounded by **ERROR**


1. Add your configuration to the [.env](.env)
```dotenv
INPUT_CSV="administrator Stems Upload List 2023_04_12-12h14m13s-QEV-151-356.csv"
MONGO_URI=mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/tv-av-prod?retryWrites=true&w=majority
MONGO_USER=user:password
```
2. Run the script
3. The output will be saved in a filename with the same name preceded by "REPORTED_"