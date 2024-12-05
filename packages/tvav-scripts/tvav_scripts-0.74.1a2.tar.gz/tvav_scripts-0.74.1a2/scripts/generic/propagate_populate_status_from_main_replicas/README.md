# propagate_populate_status_from_main_replicas

This script copies the populate status from the `main_replica` to every re-run.

## How it works

Takes a date range.

Fetches all schedules not `main_replicas` for the date range and groups them by
their `av_work`.

It then fetches the `av_work.original_schedule` and copies the populate status to all the
re-runs.

## How to make it work

Duplicate the `.env.template`, name it as `.env` and fill the env variables for your use case.
