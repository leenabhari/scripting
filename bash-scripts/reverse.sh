#!/bin/bash

if [ $# -eq 0 ];
then
    echo "Provide atleast 1 argument"
fi

for (( i=$#; i>0; i-- ))
do 
    echo -n "${!i} "
done

echo