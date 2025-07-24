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

# install dependencies
function installDeps() {
    # update pip
    ${VENV_ROOT}/bin/python -m pip install --upgrade pip
    # install cli requirements only
    ${VENV_ROOT}/bin/pip install -r requirements.txt
}

createVenv ${VENV_ROOT}
installDeps