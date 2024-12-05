# replace_music_work

This script will replace all instances of `TARGET_MUSIC_WORK` with a `FINAL_MUSIC_WORK`
for all AvWorks inside [av_works_to_be_affected.json](av_works_to_be_affected.json)

To use this script, please, fill in these 2 files:
- [.env](.env): replace all `CHANGEME` for your use case values (`TARGET_MUSIC_WORK`and
`FINAL_MUSIC_WORK` should be the MusicWork ids in string format, without the `ObjectId()`)
- [av_works_to_be_affected.json](av_works_to_be_affected.json): This file should contain a JSON list
with ids for all AvWorks to be affected in string format (not `ObjectId()`)

The `CUSTOM_PREFIX` is used to create a flag in the extras of the cues affected with
the refactor timestamp. I recommend using the ticket for this refactor.