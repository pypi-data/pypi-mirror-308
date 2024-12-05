#!/usr/bin/env bash

set -eEo pipefail

# The location of all of Sami's files
sami_dir="$1"
output_dir="$2"

if [ "$sami_dir" == "" ] || [ "$output_dir" == "" ]; then
    echo "Usage: $0 [SAMI_FILES_DIRECTORY] [OUTPUT_DIRECTORY]" >&2
    exit 1
fi

while read -r l; do
    name="$(basename "$l")"

    if [ ! -f "$output_dir"/"$name" ]; then
        # All the files we got from Sami should be amendments of existing files, so
        # this should not happen (but it does, you'll see the warnings)
        echo "WARNING: Target file ${output_dir}/${name} missing" >&2
    fi

    cp "$l" "$output_dir"/"$name"
done < <(find "$sami_dir" -name "*.xml" -not -wholename "*Reports to Gramex and Teosto - Sent 14.2.2023.zip_dir/*")
