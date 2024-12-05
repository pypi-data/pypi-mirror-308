# refactor_music_works

1. Read from CSV file "old_value" and "new_value"
2. Query DB
3. Replace in music_works
4. Return a CSV with all MusicWorks affected, with the following:
   - MusicWork id
   - field changed
   - old_value
   - new_value
5. For each line in last CSV, query all AvWorks pointing to that MusicWork.
6. Return a CSV with all AvWorks, with the following:
   - URL to the program
   - YLE program_id
   - Number of cue updated
   - MusicWork title
   - field changed
   - old_value
   - new_value