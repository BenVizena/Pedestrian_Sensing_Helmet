#! /bin/bash

while [ True ]
do
    if [[ $(ps -ef | grep python) != *'detect_live'* ]]; then
        echo "starting detect_live.py"
        $( python detect_live.py )
    else
        echo "watching..."
        sleep 5 
    fi
done
