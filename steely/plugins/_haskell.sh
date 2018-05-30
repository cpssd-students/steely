DIRECTORY="temporary"
EXECUTABLE="$DIRECTORY/main"
FILENAME="$DIRECTORY/code.hs"

function _clean_up {
    rm -rf $DIRECTORY
    mkdir $DIRECTORY
}

function _save {
    code=$(cat)
    echo "$code" > $FILENAME
}

function _compile {
    echo
    echo "*Compiler Output:*"
    ghc -o $EXECUTABLE $FILENAME
}

function _run {
    echo
    echo "*Program Output:*"
    local secondsToWait=4
    local whitelist="$(pwd)/$DIRECTORY"

    timeout $secondsToWait firejail --quiet --noprofile --whitelist=$whitelist ./$EXECUTABLE || _checkTimeout
}

function _checkTimeout {
    local exitCode=$?
    if [[ $exitCode -eq 124 ]]; then
        echo "Program timed out. Don't be cheeky."
    fi
}

set -e
trap _clean_up EXIT

_clean_up
_save
_compile
_run
