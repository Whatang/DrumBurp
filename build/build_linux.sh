#!/bin/bash
#
# Build DrumBurp for Linux
#
# This script just runs pyinstaller with the correct options, then copies the result to the
# output directory.
if [ -z "${GITHUB_WORKSPACE}"]
then
    this_script=$(abspath $0)
    workspace_root=$(dirname $this_script)
else
    workspace_root="${GITHUB_WORKSPACE}"
fi
pyinstaller -w -F -y --distpath "$workspace_root/build/dist" --specpath "$workspace_root/build/tmp" --workpath "$workspace_root/build/tmp" -i "$workspace_root/src/GUI/Icons/drumburp.ico" "$workspace_root/src/DrumBurp.py"
cp "$workspace_root/build/dist/..." "$workspace_root/build/output"