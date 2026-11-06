#!/bin/bash

# Loop through all directories starting with 3 digits and an underscore
for dir in [0-9][0-9][0-9]_*/; do
    if [[ -d "$dir" ]]; then
        # Remove trailing slash from the glob match
        dir="${dir%/}"
        
        # Slice out the first 4 characters (the 3 digits and the underscore)
        new_dir="${dir:4}"
        
        # Check if the directory is inside a Git repository to preserve history
        if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
            echo "Git moving: $dir -> $new_dir"
            git mv "$dir" "$new_dir"
        else
            echo "Moving: $dir -> $new_dir"
            mv "$dir" "$new_dir"
        fi
    fi
done

