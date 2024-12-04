#!/bin/sh

# Check if simple-word-url-shortener is already installed on docker
if [ "$(docker ps -aq -f name=simple-word-url-shortener)" ]; then
    read -p "There is an existing one, do you want to reinstall and reconfigure it? (yes/no): " confirm
    if [ $confirm == "yes" ]; then
        echo ""
        echo "Stopping please wait patiently..."
        docker stop simple-word-url-shortener
        docker-compose down
        docker rm simple-word-url-shortener
    else
        echo "Exiting..."
        echo ""
        exit 1
    fi
fi

# Check if python3 is installed, if not then do auto install
if ! command -v python3 &> /dev/null
then
    if ! command -v apt-get &> /dev/null
    then
        echo ""
        echo "Python3 not found on your system and the automated install script is only for debian-based systems."
        echo "Please install python3 manually."
        exit 1
    fi
    echo ""
    read -p "Python3 is not installed. Do you want to install it? (yes/no): " confirm
    if [ $confirm == "yes" ]; then
        sudo apt-get update
        sudo apt-get install python3
    else
        echo ""
        echo "Please install python3 and run this script again."
        exit 1
    fi
    exit 1
fi

# Generate .env and set baseurl and link it to app/.env
echo ""
echo "Please enter the base URI that is used to show on the webpage of the generated link (including https:// or http:// and the port number behind)."
echo "If you are routing this thorugh a proxy, you should enter the proxied information."
echo ""
read -p "Please enter: " baseurl
echo "BASE_URL=$baseurl" > .env

# Dictionary confirmation
echo ""
echo "Please note that if you decided that you want to change the dictionary, you need to run this scirpt again and it'll cause you to loose every shortened uri you've generated."
read -p "If you've decided that the dictionay of dictionary.txt is exactly what you want, please enter 'yes' to continue: " confirm
if [ $confirm != "yes" ]; then
    echo "Please modify dictionary.txt and run setup.sh again."
    exit 1
fi

# Remove old database
rm app/python/data.db

# Initialize database
python3 init_db.py

# Set permission
chmod -R 777 app

# Docker compose up
echo ""
docker-compose up --build -d

