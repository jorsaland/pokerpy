Clear-Host

powershell {

    ./env/Scripts/Activate.ps1

    python -m unittest discover tests/unit

    deactivate

}