#!/bin/bash
# We suppose you have finished all the config item in .gitmodule file.

# Clone all the submodules (init and update based on .gitmodules)
git config --file .gitmodules --name-only --get-regexp "submodule\..*\.url" | \
while read submodule; do
    name=$(echo $submodule | sed 's/submodule\.\(.*\)\.url/\1/')
    url=$(git config --file .gitmodules "$submodule")
    echo -e "Initializing submodule, name: $name, url: $url"
    git submodule add "$url" "$name"
    git submodule init "$name"
done
git submodule update