#!/bin/bash
#
# Build DrumBurp for Linux
#
# This script just runs pyinstaller with the correct options, then copies the result to the
# output directory.
this_script=$(realpath $0)
workspace_root=$(dirname $(dirname $this_script))
echo "Workspace root is ${workspace_root}"

pyinstaller -w -F -y  --hidden-import=PyQt4 --distpath "$workspace_root/build/dist" --specpath "$workspace_root/build/tmp" --workpath "$workspace_root/build/tmp" -i "$workspace_root/src/GUI/Icons/drumburp.ico" "$workspace_root/src/DrumBurp.py"
