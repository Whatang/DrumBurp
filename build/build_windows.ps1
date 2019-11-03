Set-Item Env:PYTHONIOENCODING UTF-8

$workspace_root = Split-Path -Parent "$PSScriptRoot"
Write-Output "$workspace_root"
if (!(Test-Path "$workspace_root\build\dist" -PathType Container)) {
    New-Item -ItemType Directory -Force -Path "$workspace_root\build\dist"
}
if (!(Test-Path "$workspace_root\build\output" -PathType Container)) {
    New-Item -ItemType Directory -Force -Path "$workspace_root\build\output"
}

& pyinstaller -w -D -y --distpath "$workspace_root\build\dist" --specpath "$workspace_root\build\tmp" --workpath "$workspace_root\build\tmp" -i "$workspace_root\src\GUI\Icons\drumburp.ico" "$workspace_root\src\DrumBurp.py"
Copy-Item "$workspace_root\COPYING.txt" "$workspace_root\build\dist"
Copy-Item "$workspace_root\build\DrumBurp.nsi" "$workspace_root\build\dist\"
Set-Location "$workspace_root\build\dist"
& "C:\Program Files (x86)\NSIS\makensis.exe" "$workspace_root\build\dist\DrumBurp.nsi"
Move-Item DrumBurp*setup.exe "$workspace_root\build\output"
Set-Location "$workspace_root"

