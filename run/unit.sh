# Move to project location

script_location=$(dirname ${0})

cd $script_location
cd ..

# Run unit tests and exit

source ./env/bin/activate
clear
python -m unittest discover tests/unit

printf "\n\n"
echo -n "--- ENTER ---"
read