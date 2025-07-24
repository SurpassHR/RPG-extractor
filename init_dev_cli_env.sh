#!/bin/bash
# Suggest using git-bash to execute
# This script is used for server execution environment (non-gui env)

# global constants
VENV_ROOT=./.venv
DOT_GIT_FILE=./.git
DOT_GIT_EXCLUDE_LIST=(
    "__pycache__"
    ".history"
    ".venv"
)

# check if function's in-params number is valid
function checkParamNum() {
    if [ $# -ne 2 ]; then
        echo -e "need 2 params num for comparison"
    fi

    argNum=$1
    expectArgNum=$2
    if [ ${argNum} -ne ${expectArgNum} ]; then
        echo -e "in-params number is not valid, expect: ${expectArgNum}, actual: ${argNum}"
        return 1
    fi
}

# create python virtual environment
function createVenv() {
    expectArgNum=1
    checkParamNum $# ${expectArgNum}

    venvPath=$1
    if [ -d "${venvPath}" ]; then
        echo "venv already exists"
    else
        echo "Creating venv"
        python -m venv ${venvPath}
    fi
}

# activate venv
function activateVenv() {
    expectArgNum=1
    checkParamNum $# ${expectArgNum}

    venvPath=$1
    case "$OSTYPE" in
        linux-gnu)
            source .venv/bin/activate
            ;;
        *)
            source .venv/Scripts/activate
            ;;
    esac
}

# install dependencies
function installDeps() {
    # update pip
    python -m pip install --upgrade pip
    # install cli requirements only
    pip install -r requirements.txt
}

createVenv ${VENV_ROOT}
activateVenv ${VENV_ROOT}
installDeps