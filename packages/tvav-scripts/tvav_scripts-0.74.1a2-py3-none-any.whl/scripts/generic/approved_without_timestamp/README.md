# approved_without_timestamp

Required for YLE-2009.

This script can be used to generate a CSV report of the cuesheets which are approved in the database but have no approval timestamp.


## Algorithm

- Query AvWorks matching:
    - "approved": true
    - "history_info.approved_change": null
    - "history_info.creator.updated_at": {$gte: START_TIME}
- For each AVWork, insert a new row in the CSV containing all values specified in the HEADERS variable.
- Note: The schedule level fields are fetched from the first Schedule found and will default to "-" if there is no schedule linked to the AvWork.
