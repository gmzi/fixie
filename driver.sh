# This driver grabs the file path from Automator and passes it to fixie.

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

# launch fixie:
osascript <<EOD
tell application "System Events"
    display dialog "Fixie is working..." giving up after 1
end tell
EOD

FILE_PATH=$1

source venv/bin/activate

python3 app.py "$FILE_PATH"

deactivate

open './output'