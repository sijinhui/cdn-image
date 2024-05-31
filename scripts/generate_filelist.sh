#!/bin/sh

# Find all directories in the project
#directories=../$(find . -type d)

generate_file_list() {
    local dir=\$1
    local file_list="$dir/file_list.txt"

    echo "Generating $file_list..."

    # Find all non-hidden files and directories, ignoring the hidden ones
    find "$dir" -type f -not -path '*/\.*' -exec basename {} \; > "$file_list"
}

export -f generate_file_list

# Find all directories and generate file lists
find . -type d -not -path '*/\.*' -exec bash -c 'generate_file_list "\$0"' {} \;

# Add the generated file_list.txt files to the staging area
git add $(find . -name 'file_list.txt')
