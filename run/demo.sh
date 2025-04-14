# Define version and demo literal

if [ $1 ]
then version=$1
else echo -n "version: "; read version
fi

if [ $2 ]
then literal=$2
else echo -n "literal: "; read literal
fi

# Move to project location

script_location=$(dirname $0)

cd $script_location
cd ..

# Run demo and exit

filepath=tests/demos/demo-${version}-${literal}.py

clear
echo --------------------------------------------------------------
printf "\n$filepath\n\n"
echo --------------------------------------------------------------
printf "\n\n\n"

source ./env/bin/activate
python $filepath