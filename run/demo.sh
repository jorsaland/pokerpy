if [ $1 ]
then version=$1
else printf "version="; read version
fi

if [ $2 ]
then literal=$2
else printf "literal="; read literal
fi

filepath=tests/demos/demo-${version}-${literal}.py

echo ---------------------------
echo $filepath
echo ---------------------------

source ../env/bin/activate
clear
python $filepath