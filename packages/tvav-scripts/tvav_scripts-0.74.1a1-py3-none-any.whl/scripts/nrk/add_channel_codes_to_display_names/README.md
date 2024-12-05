# Add channel codes to display names

## Context
When generating reports for a channel, the output filename will have a specific identifier which represents the channel. I.E.: Podcast -> PODCASTS

### Input
1. Create a CSV file containing 2 columns: Display Name (the name you can see for the channel in the UI) and Channel Codes (the identifier you want in the report).
2. Fill in the **CHANNEL_CSV_PATH** parameter in the [.env](.env) file.
3. The file should have headers (or a blank row at the start).
4. The column headers text does not need to match any special format, data will be read in order: display (column A), code (column B).


### Output
1. A csv will be created after a successful run of this script.
2. This csv will provide the list of matched channels, the newly set codes, the previous ones and whether they were edited or not.
3. By default, the file will be named: **edited_channels.csv** and placed in this same folder.
4. You can customise the output path by editing the **OUTPUT_FILENAME** parameter in the [.env](.env) file.
