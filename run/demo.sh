if [ $1 ]
then version=$1
else printf "version:"; read version
fi

if [ $2 ]
then literal=$2
else printf "literal:"; read literal
fi

clear
filepath=tests/demos/demo-${version}-${literal}.py

echo --------------------------------------------------------------
printf "\n$filepath\n\n"
echo --------------------------------------------------------------
printf "\n\n\n"

source ./env/bin/activate
python $filepath