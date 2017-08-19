#!/bin/bash

function print_green(){
    echo -e "\033[32m$1\033[39m"
}

INSTALL_SYSTEM_DEPENDENCIES=true
INSTALL_PIP=true
INSTALL_BOWER=true
INSTALL_NPM=true
TRANSLATE=true
BUILD_JAVASCRIPT=true

#!/bin/sh

case "$(uname -s)" in

   Darwin)
     OS='Darwin'
     ;;

   Linux)
     OS='Linux'
     ;;

   *)
    echo "OS not supported"
    exit
    ;;
esac


while getopts “napbj” OPTION
do
    case $OPTION in
        a)
             print_green "only install aptitude"
             INSTALL_SYSTEM_DEPENDENCIES=true
             INSTALL_PIP=false
             INSTALL_BOWER=false
             INSTALL_NPM=false
             TRANSLATE=false
             BUILD_JAVASCRIPT=false
             ;;
        p)
             print_green "only pip install"
             INSTALL_SYSTEM_DEPENDENCIES=false
             INSTALL_PIP=true
             INSTALL_BOWER=false
             INSTALL_NPM=false
             TRANSLATE=false
             BUILD_JAVASCRIPT=false
             ;;
        b)
             print_green "only bower install"
             INSTALL_SYSTEM_DEPENDENCIES=false
             INSTALL_PIP=false
             INSTALL_BOWER=true
             INSTALL_NPM=false
             TRANSLATE=false
             BUILD_JAVASCRIPT=false
             ;;
        n)
             print_green "only node install"
             INSTALL_SYSTEM_DEPENDENCIES=false
             INSTALL_PIP=false
             INSTALL_BOWER=false
             INSTALL_NPM=true
             TRANSLATE=false
             BUILD_JAVASCRIPT=false
             ;;
        j)
             print_green "only npm run build"
             INSTALL_SYSTEM_DEPENDENCIES=false
             INSTALL_PIP=false
             INSTALL_BOWER=false
             INSTALL_NPM=false
             TRANSLATE=false
             BUILD_JAVASCRIPT=true
             ;;
        ?)
             print_green "fail"
             exit
             ;;
     esac
done

if  $INSTALL_SYSTEM_DEPENDENCIES ; then
    if [ "$OS" == "Darwin" ] ; then
        print_green "Installing python 3"
        brew install python3

        print_green "Installing virtualenv"
        pip install virtualenv
    else
        print_green "Installing aptitude dependencies"

        # Install base packages
        sudo apt-get -y install python-pip python-virtualenv python3-dev build-essential

        print_green "Installing image libraries"
        # Install image libs
        sudo apt-get -y install libjpeg-dev zlib1g-dev zlib1g-dev

        print_green "Installing translation libraries"
        sudo apt-get -y install gettext
    fi

    print_green "Are you going to use postgre for your database? [Y/n]"
    read INSTALL_POSTGRE

    if [[ "$INSTALL_POSTGRE" == "Y" ||  "$INSTALL_POSTGRE" == "y" ||  "$INSTALL_POSTGRE" == "" ]]
    then
        INSTALL_POSTGRE=true
        if [ "$OS" == "Darwin" ] ; then
            if brew ls --versions postgresql > /dev/null ; then
                echo 'postgresql is already installed'
            else
                brew install postgresql
            fi
        else
            ./install/postgres.sh
        fi
    fi

    if [ ! -d ".env" ]; then
        print_green "set a new virtual environment"
        virtualenv -p python3 .env
    fi
fi
if  $INSTALL_PIP ; then
    print_green "Installing pip requirements on requirement.txt"

    # activate the environment
    source .env/bin/activate

    # install setuptools
    pip install --upgrade setuptools

    # upgrade pip
    pip install --upgrade pip

    # install pip requirements in the virtual environment
    .env/bin/pip install --requirement requirements.txt
fi

# create the local_settings file if it does not exist
if [ ! -f ./project/settings/local_settings.py ] ; then
    cp project/local_settings.py.default project/local_settings.py

    if [ INSTALL_POSTGRE ] ; then
        EXP="s/database-name/${PWD##*/}/g"
        echo $i|sed -i '' $EXP project/local_settings.py

        print_green "remember to configure in project/local_setings.py your database"
    else
        EXP="s/postgresql_psycopg2/sqlite3/g"
        echo $i|sed -i '' $EXP project/local_settings.py

        EXP="s/database-name/\/tmp/${PWD##*/}.sql/g"
        echo $i|sed -i '' $EXP project/local_settings.py
    fi
fi

# Change the project/settings.py file if it contains the CHANGE ME string
if grep -q "CHANGE ME" "project/settings.py"; then
    print_green "Generate secret key"
    # change the SECRET_KEY value on project settings
    python manage.py generatesecretkey
fi


if  $INSTALL_NPM ; then
    # package.json modification
    EXP="s/NAME/${PWD##*/}/g"
    print_green $i|sed -i '' $EXP package.json
    EXP="s/HOMEPAGE/https:\/\/bitbucket.org\/magnet-cl\/${PWD##*/}/g"
    print_green $i|sed -i '' $EXP package.json

    npm install
fi
