#!/bin/bash

# create python virtual environment
if [ -d "./.venv" ]; then
    echo "venv already exists"
else
    echo "Creating venv"
    python -m venv .venv
fi

# activate venv
case "$OSTYPE" in
    linux-gnu)
        source .venv/bin/activate
        ;;
    *)
        source .venv/Scripts/activate
        ;;
esac

# install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

git_exclude_content=`cat .git/info/exclude | grep -E '__pycache__|.history|.venv'`

if [[ -n $git_exclude_content ]]; then
    echo "git exclude already contains __pycache__, .history, and .venv"
else
    echo "\n"
    echo "__pycache__" >> .git/info/exclude
    echo ".history" >> .git/info/exclude
    echo ".venv" >> .git/info/exclude
    echo "Added __pycache__, .history, and .venv to git exclude"
fi