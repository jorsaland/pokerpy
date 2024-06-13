# Move to project location

script_location=$(dirname ${0})

cd $script_location
cd ..

# Create virtual environment and revert location

echo "Creating Python 3.12 virtual environment..."
python3.12 -m venv ./env