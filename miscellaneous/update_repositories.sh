#!/bin/bash

# Define the base directory
base_directory=/home/brandon/Repositories

# Navigate to the base directory
cd "$base_directory" || exit

# Iterate through each directory
for dir in */; do
    # Trim trailing slash to get the directory name
    dir_name="${dir%/}"

    # Navigate into the directory
    cd "$dir_name" || continue

    # Check if the directory is a git repository
    if [ -d ".git" ]; then
        # Execute git pull
        echo "Pulling changes in $dir_name..."
        git pull
    else
        echo "$dir_name is not a git repository."
    fi

    # Return to the base directory
    cd "$base_directory" || exit
done

