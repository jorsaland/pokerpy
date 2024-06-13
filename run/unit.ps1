# Move to project location

$script_location = Split-Path $MyInvocation.MyCommand.Path -Parent

Push-Location $script_location
Push-Location ../

# Run unit tests

Clear-Host

./env/Scripts/Activate.ps1
python -m unittest discover tests/unit
deactivate

# Revert location and exit

Pop-Location
Pop-Location

Write-Host `n
Write-Host "--- ENTER ---" -NoNewLine
$Host.UI.ReadLine()