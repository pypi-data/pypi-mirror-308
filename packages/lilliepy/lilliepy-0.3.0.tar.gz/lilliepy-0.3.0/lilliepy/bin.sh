#!/bin/bash

blank='\033[0m'
error='\033[31m'
success='\033[32m'
load='\033[34m'

echo -e "${load}Initializing Lilliepy App...${blank}"

git clone https://github.com/websitedeb/Lilliepy-2.0
if [ $? -eq 0 ]; then
    mv "Lilliepy-2.0" "app"
    if [ $? -eq 0 ]; then
        echo -e "${load}Downloading dependencies...${blank}"
        cd app
        pip install -r requirements.txt

        if [ $? -eq 0 ]; then
            echo -e "${success}Created Lilliepy App!${blank}"
            read -p "Press any key to continue..."
        else
            echo -e "${error}An error occurred while downloading the dependencies...${blank}"
            read -p "Press any key to continue..."
        fi
    else
        echo -e "${error}An error occurred while renaming the app...${blank}"
        read -p "Press any key to continue..."
    fi
else
    echo -e "${error}An error occurred while creating the app...${blank}"
    read -p "Press any key to continue..."
fi

clear
