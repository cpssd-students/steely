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
    ghc -o $EXECUTABLE $FILENAME
}

function _run {
    echo
    echo "Output:"
    ./$EXECUTABLE
}

set -e
trap _clean_up EXIT

_clean_up
_save
_compile
_run
