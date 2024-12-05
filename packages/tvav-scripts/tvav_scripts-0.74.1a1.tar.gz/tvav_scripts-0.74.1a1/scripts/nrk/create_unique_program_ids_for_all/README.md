# create_unique_program_ids_for_all

This script:

1. Queries for all AvWorks with no `work_ids["program_id"]`
2. Generates unique `program_id`
3. Saves it in `work_ids["program_id"]`

Fill the [.env](.env) with the right values.