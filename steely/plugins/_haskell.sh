set -e
DIRECTORY="temporary"
EXECUTABLE="$DIRECTORY/main"
FILENAME="$DIRECTORY/code.hs"

# Clean up
rm -rf $DIRECTORY
mkdir $DIRECTORY

# Read code from stdin
code=$(cat)

# Save code to disk
echo "$code" > $FILENAME

# Compile code
ghc -o $EXECUTABLE $FILENAME

# Run code
./$EXECUTABLE
