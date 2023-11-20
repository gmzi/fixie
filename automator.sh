# AUTOMATOR QUICK ACTION SETUP FOR MAC
# -------------------------------------

# Step 1: Open Automator
# ----------------------
# On your Mac, open the Automator.app.
# Select "Quick Action" to create a new quick action workflow.

# Step 2: Configure Workflow
# --------------------------
# In the Automator interface:
# - On the top right: Set "Workflow receives current" to "files or folders" in "Finder".
# - Drag the action "Run Shell script" into the workflow area.

# Step 3: Shell Script Settings
# -----------------------------
# Inside the "Run Shell script" action:
# - Set the shell type (e.g., /bin/bash).
# - Set "Pass Input" to "as arguments".
# - Paste your shell script into the script area. Here's mine as an example:

#!/bin/bash
for f in "$@"
do
	cd ~/projects/fixie/
	./driver.sh $f
done

# - Replace <~/projects/fixie/> with the path to your project folder.

# Step 4: Save and Authorize
# --------------------------
# - Name your quick action as desired for display in the quick actions menu.
# - Save and exit Automator.
# - Authorize your bash script for execution.
# - In case you use it, authorize ./driver.sh for execution.

# Step 5: Edit or Remove Quick Action
# ------------------------------------
# To modify or delete this Automator quick action later:
# - Navigate to /Library/Services.
# - Find and modify or delete your_file.workflow.