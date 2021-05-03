#!/bin/bash

function activate {
            source env/bin/activate
}

if [ ! -d "./env" ];
then

    echo "Creating environment..."
    python3.8 -m venv env
    activate
    python3.8 -m pip install -r requirements.txt

else

    echo "Environment already exists"
    activate

fi

echo "Script will be run in the background. Please run: watch tail api_log.txt"
nohup python3.8 -u ./api.py > api_log.txt 2>&1 &
#python3.8 ./api.py

deactivate