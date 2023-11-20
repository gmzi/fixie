# Purpose

# this is a backupt of the shell script that Automator.app runs on mac, it is aimed to 
# be added to Mac Finder's Quick Actions menu, so when a user right clicks on a file, 
# the option to run this program is showed and there's no need to drag and drop the file 
# or manage windows.

# Usage



# On mac, open Automator.app. -> Quick Action -> 
# Set On top right: "Workflow receives current" 
# set to "files or folders", "in" "Finder". Then drag the action "Run Shell script". Inside
# the script, set shell and "Pass Input: as arguments". Then paste the shell script below, replacing <~/projects/fixie_2/> with your project's path. Name
# the quick action the way you want it to be displayed in quick actions menu, save and quit.
# To remove or edit this Automator quick action, go to /Library/Services and find your_file.workflow.

#!/bin/bash
for f in "$@"
do
	cd ~/projects/fixie/
	./driver.sh $f
done
