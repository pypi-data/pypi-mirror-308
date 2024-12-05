# unapproved_after_reported

Requested in YLE-2186. Related to YLE-2107.

This script serves to generate a CSV report of YLE programs in a user-specified time period which are linked to an AV-Work that turned to approved=False and reported=True after being reported.

## Steps

- Queries schedule candidates in user-defined time-period
- Queries av_works matching

      - "reported": true
      - "approved": false

- Computes schedules which are linked to matched av_works
- For each schedule writes a new line to CSV file