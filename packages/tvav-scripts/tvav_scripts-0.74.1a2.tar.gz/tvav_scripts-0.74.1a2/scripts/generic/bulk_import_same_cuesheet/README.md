# bulk_import_same_cuesheet

Required for TVAV-10401.

This script can be used to bulk import the same cuesheet
for many Schedules at once.

It creates a new file in tv-av-prod with the right
namespace, file path, user_id and schedule_id
and then triggers the file processor that then triggers
the import_cuesheet chain.


## Algorythm

- query FILE_ID_TO_USE
- read INPUT_FILE_WITH_SCHEDULE_IDS_AS_STR
- for each SCHEDULE_ID:
    - dup file with changes:
        - delete history
        - update data.schedule_id = <schedule_id>
        - update data.FLAG = True
        - save file
- trigger file processor for new files
