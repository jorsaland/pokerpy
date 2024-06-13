# Move to project location

$script_location = Split-Path $MyInvocation.MyCommand.Path -Parent

Push-Location $script_location
Push-Location ../

# Create virtual environment and revert location

Write-Output "Creating Python 3.12 virtual environment..."
py -3.12 -m venv ./env

Pop-Location
Pop-Location