#!/bin/bash

function print_green(){
    echo -e "\033[32m$1\033[39m"
}

function replace(){
    echo $1 $2
    if [ "$OS" == "Darwin" ] ; then
        echo $i|sed -i '' $1 $2
    else
        echo $i|sed -i $1 $2
    fi
}

INSTALL_SYSTEM_DEPENDENCIES=true
PIPENV_INSTALL=true
INSTALL_BOWER=true
INSTALL_YARN=true
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


while getopts “yapbj” OPTION
do
    case $OPTION in
        a)
             print_green "only install aptitude"
             INSTALL_SYSTEM_DEPENDENCIES=true
             PIPENV_INSTALL=false
             INSTALL_BOWER=false
             INSTALL_YARN=false
             TRANSLATE=false
             BUILD_JAVASCRIPT=false
             ;;
        p)
             print_green "only pip install"
             INSTALL_SYSTEM_DEPENDENCIES=false
             PIPENV_INSTALL=true
             INSTALL_BOWER=false
             INSTALL_YARN=false
             TRANSLATE=false
             BUILD_JAVASCRIPT=false
             ;;
        b)
             print_green "only bower install"
             INSTALL_SYSTEM_DEPENDENCIES=false
             PIPENV_INSTALL=false
             INSTALL_BOWER=true
             INSTALL_YARN=false
             TRANSLATE=false
             BUILD_JAVASCRIPT=false
             ;;
        y)
             print_green "only yarn install"
             INSTALL_SYSTEM_DEPENDENCIES=false
             PIPENV_INSTALL=false
             INSTALL_BOWER=false
             INSTALL_YARN=true
             TRANSLATE=false
             BUILD_JAVASCRIPT=false
             ;;
        j)
             print_green "only npm run build"
             INSTALL_SYSTEM_DEPENDENCIES=false
             PIPENV_INSTALL=false
             INSTALL_BOWER=false
             INSTALL_YARN=false
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
        print_green "Installing pyenv"
        brew install pyenv

        print_green "Installing pipenv"
        brew install pipenv
    else
        print_green "Installing python 3.6"
        sudo add-apt-repository ppa:deadsnakes/ppa
        sudo apt-get update
        sudo apt-get -y install python3.6 python3.6-dev

        print_green "Installing aptitude dependencies"
        sudo apt-get -y install python-pip python-virtualenv build-essential

        print_green "Installing image libraries"
        # Install image libs
        sudo apt-get -y install libjpeg-dev zlib1g-dev zlib1g-dev

        print_green "Installing translation libraries"
        sudo apt-get -y install gettext

        print_green "Installing pipenv"
        sudo pip install pipenv
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

    viertual_env_directory=`pipenv --venv`
    if [ ! -d "$viertual_env_directory" ]; then
        print_green "set a new python 3.6 project with pipenv"
        pipenv --python 3.6
    fi
fi

if  $PIPENV_INSTALL ; then
    print_green "Installing python requirements with pipenv defined on Pipfile"

    # install python requirements
    pipenv install
fi

# create the local_settings file if it does not exist
if [ ! -f ./project/settings/local_settings.py ] ; then
    print_green "Generating local settings"

    cp project/local_settings.py.default project/local_settings.py

    if [ INSTALL_POSTGRE ] ; then
        replace "s/database-name/${PWD##*/}/g" project/local_settings.py

        print_green "remember to configure in project/local_setings.py your database"
    else
        replace "s/postgresql_psycopg2/sqlite3/g" project/local_settings.py

        replace "s/database-name/\/tmp/${PWD##*/}.sql/g" project/local_settings.py
    fi
fi

# Change the project/settings.py file if it contains the CHANGE ME string
if grep -q "CHANGE ME" "project/local_settings.py"; then
    print_green "Generate secret key"

    # change the SECRET_KEY value on project settings
    pipenv run python manage.py generatesecretkey
fi


if  $INSTALL_YARN ; then
    print_green "Installing yarn dependencies"

    # package.json modification
    replace "s/NAME/${PWD##*/}/g" package.json
    replace "s/HOMEPAGE/https:\/\/bitbucket.org\/magnet-cl\/${PWD##*/}/g" package.json

    yarn install
fi
