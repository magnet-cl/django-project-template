#!/bin/bash
sudo apt-get -y install postgresql
sudo apt-get -y install libpq-dev

function print_green(){
    echo -e "\e[32m$1\e[39m"
}

print_green "Would you like to set a password for your postgres user? [N/y]"
read SET_POSTGRES_PASSWORD
if [[ "$SET_POSTGRES_PASSWORD" == "y" ]]
then
    sudo -u postgres createuser --superuser $USER
    echo "\password $USER" | sudo -u postgres psql
    createdb $USER
fi
