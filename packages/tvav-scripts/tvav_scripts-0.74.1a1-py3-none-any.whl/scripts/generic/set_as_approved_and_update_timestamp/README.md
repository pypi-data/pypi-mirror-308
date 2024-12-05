# set_as_approved_and_update_timestamp

This script was requested for ticket [YLE-2009](https://bmat-music.atlassian.net/browse/YLE-2009).

---

## Description
This script takes a list of `work_ids` to fetch 1 AvWork per each and approves them, updates their status and
the history_info.

## How it works
- Loads the configuration from the environment.
    - `work_id` can take the value you need by I suggest using `program_id` (`plasma_id` for YLE)
- Reads from a CSV file
- Queries the DB
- Updates the fields
- Reloads them from the DB
- Generates a report with the `approved`, `status` and `history_info` values.
