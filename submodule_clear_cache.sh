#!/bin/bash
if [ -f .gitmodules ]; then
    git submodule deinit --all -f
fi

git config --file .gitmodules --get-regexp 'submodule\..*\.path' | while read key path; do
    mod_name=$(echo $key | sed 's/submodule\.\(.*\)\.path/\1/')
    rm -rf ".git/modules/$mod_name"
done