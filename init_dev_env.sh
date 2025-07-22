#!/bin/bash
# suggest using git-bash to execute

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
    # install all requirements recursively
    find . -name "requirements.txt" -exec pip install -r {} \;
}

# table-driven add some exclude items in .git/info/exclude
function addExcludes() {
    if [ -d "${DOT_GIT_FILE}" ]; then
        exclude_file="${DOT_GIT_FILE}/info/exclude"

        # check if exist
        found=0
        if [ -f "${exclude_file}" ]; then
            for pattern in "${DOT_GIT_EXCLUDE_LIST[@]}"; do
                if grep -qF "${pattern}" "${exclude_file}"; then
                    found=1
                    break
                fi
            done
        fi

        # write exclude items into exclude file
        printf -v joined '%s, ' "${DOT_GIT_EXCLUDE_LIST[@]}"
        if [ $found -eq 1 ]; then
            echo "git exclude already contains ${joined%, }"
        else
            echo

            printf "%s\n" "${DOT_GIT_EXCLUDE_LIST[@]}" >> "${exclude_file}"

            echo "Added ${joined%, } to git exclude"
        fi
    fi
}

createVenv ${VENV_ROOT}
activateVenv ${VENV_ROOT}
installDeps
addExcludes