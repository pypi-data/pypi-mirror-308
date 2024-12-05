#!/usr/bin/env bash

set -eEo pipefail

# The location of all of the downloaded Jira attachments
jira_files_dir="$1"
output_dir="$2"

if [ "$jira_files_dir" == "" ] || [ "$output_dir" == "" ]; then
    echo "Usage: $0 [JIRA_FILES_DIRECTORY] [OUTPUT_DIRECTORY]" >&2
    exit 1
fi

while read -r l; do
    name="$(basename "$l")"

    # Undo the messed up filename produced by jira.py, back to a normal Jira name
    final_name="$(echo "$name" | python3 -c "
import sys
for line in sys.stdin:
    line = line.strip()
    parts = line.split('_')
    print('_'.join(parts[-4:]))
")"

    if [ -f "$output_dir"/"$final_name" ]; then
        echo "INFO: Skipping ${output_dir}/${final_name} because it already exists" >&2
    else
        output_path="{output_dir}/${final_name}"
        echo "INFO: Creating ${output_path}" >&2
        cp "$l" "$output_path"
    fi
done < <(find "$jira_files_dir" -name "*.xml")
