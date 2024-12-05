# update_av_work_category

This script can be used to update every candidate AvWork category in Eurosport DB.

An AvWork is considered a candidate for this script if:

- Category is `PROGRAMMES` AND
- Has at least 1 Cue with use `Live music` AND
- At least one of the following is True (OR):
    - `original_title` contains any pattern from `IS_LIVE_TITLE_INCLUDES` AND NONE from `IS_NOT_LIVE_TITLE_INCLUDES`
    - `eurosport_tag` not amongb `IS_LIVE_EUROSPORT_TAG_EQUALS`
    - `original_title` contains any pattern from `IS_LIVE_EUROSPORT_TAG_TITLE_EXCLUDES`

Then, for said candidates, we call `update_av_work_category` method from Eurosport's custom MatchImporter, which should update:

- `AvWork.category` --> `PROGRAMMES - Live`
- `Schedule.aggregations.category` --> `PROGRAMMES - Live`
- `Schedule.extras["live_music_checked"]` --> `True`
