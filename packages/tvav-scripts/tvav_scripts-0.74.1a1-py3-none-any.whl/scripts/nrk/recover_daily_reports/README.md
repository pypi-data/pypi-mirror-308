# Recover daily reports

The purpose of this script is to process files in an S3 bucket, update their metadata in a MongoDB database, and optionally create backups of files before deleting them. 
The script provides flexibility through command-line arguments to control the processing behavior such as filtering files by ID, performing a dry run, creating backups, and writing logs to a file.

The ticket: [NRK - Recover overwritten daily reports](https://bmat-music.atlassian.net/browse/TVAV-10018)
