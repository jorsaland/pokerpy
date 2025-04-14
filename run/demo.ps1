# Define version and demo literal

param([string]$version, [string]$literal)

if (-not $version)
    {$version = Read-Host "version"}

if (-not $literal)
    {$literal = Read-Host "literal"}

# Move to project location

$script_location = Split-Path $MyInvocation.MyCommand.Path -Parent

Push-Location $script_location
Push-Location ../

# Run demo

$demo_filepath = "tests/demos/demo-$version-$literal.py"

Clear-Host
Write-Host --------------------------------------------------------------
Write-Host "`n$demo_filepath`n"
Write-Host --------------------------------------------------------------
Write-Host `n`n

./env/Scripts/Activate.ps1
python $demo_filepath
deactivate

# Revert location and exit

Pop-Location
Pop-Location