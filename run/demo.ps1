param([string]$version, [string]$literal)

if (-not $version)
    {$version = Read-Host "version"}

if (-not $literal)
    {$literal = Read-Host "literal"}

Clear-Host
$env:demo_filepath = "tests/demos/demo-$version-$literal.py"

powershell {

    Write-Output --------------------------------------------------------------
    Write-Output "`n$env:demo_filepath`n"
    Write-Output --------------------------------------------------------------
    Write-Output `n`n

    ./env/Scripts/Activate.ps1

    python $env:demo_filepath

    deactivate

}

$env:demo_filepath = ""