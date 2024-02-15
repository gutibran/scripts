#!/bin/bash
echo "Enter a directory path"
read directory
for filename in "$directory"/*; do
    if [[ -f "$filename" ]]; then
        new_filename="${filename%.*}.jpg"
        mv -n "$filename" "$new_filename"
    fi
done
echo "File extensions updated successfully."
