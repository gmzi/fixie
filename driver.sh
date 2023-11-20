# This driver grabs the file path from Automator and passes it to Fixie.

#!/bin/bash

# Check if a directory path is provided
if [ "$#" -ne 1 ]; then
    echo "Missing argument: $0 <directory-path>"
    exit 1
fi

# confirm before launching:
# osascript <<EOD
# tell application "System Events"
#     display dialog "Launch Fixie?"
# end tell
# EOD

# Display dialog before launching fixie:
osascript <<EOD
tell application "System Events"
    display dialog "Fixie is working..." giving up after 1
end tell
EOD

FILE_PATH=$1

source venv/bin/activate

python3 app.py "$FILE_PATH"

# if app.py script fails will exit with a non-zero status
STATUS=$?

deactivate

if [ $STATUS -ne 0 ]; then
    osascript -e 'tell app "System Events" to display dialog "Fixie quit with status 1. Check your .pdf please"'
    exit 1
fi

open './output'