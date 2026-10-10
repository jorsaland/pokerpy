# Move to project location

script_location=$(dirname ${0})

cd $script_location
cd ..

# Run unit tests and exit

source ./env/bin/activate
clear

if python -c "import pytest" &> /dev/null; then
    python -m pytest
else
    python -m unittest discover tests/unit
fi

printf "\n\n"
echo -n "--- ENTER ---"
read