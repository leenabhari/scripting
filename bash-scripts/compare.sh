#!/bin/bash

if [ $# -ne 2 ]; 
then
    echo "You must provide 2 files"
fi

if [ ! -f $1 ] || [ ! -f $2 ]
then
    echo "Argument provided must be a file"
fi

grep -Fxf "$1" "$2"