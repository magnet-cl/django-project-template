#!/bin/bash

function print_green(){
    echo -e "\033[32m$1\033[39m"
}

function print_red(){
    echo -e "\033[31m$1\033[39m"
}

function print_blue(){
    echo -e "\033[34m$1\033[39m"
}

function makemessages {
    if [ -d $1 ]; then
        cd $1

        mkdir -p locale

        django-admin.py makemessages -l es -e pug,html,txt,py
        diff=$(git diff --numstat locale/es/LC_MESSAGES/django.po)
        lineCount=(${diff// / })

        if [ $lineCount ] ; then
            if [ $lineCount == 1 ] ; then
                git checkout locale/es/LC_MESSAGES/django.po
            fi
        fi

        django-admin.py makemessages -d djangojs -l es -i "static/bower_components" -e pug,js

        if [ -f locale/es/LC_MESSAGES/djangojs.po ]; then
            diff=$(git diff --numstat locale/es/LC_MESSAGES/djangojs.po)
            lineCount=(${diff// / })
            if [ $lineCount ] ; then
                if [ $lineCount == 1 ] ; then
                    git checkout locale/es/LC_MESSAGES/djangojs.po
                fi
            fi
        fi

        cd ..
    else
        print_red "folder $1 does not exist"
    fi
}

function translate {
    print_green "translating $1"
    if $COMPILE ; then
        cd $1
        django-admin.py compilemessages
        cd ..
    else
        makemessages $1
    fi
}

COMPILE=false

while getopts “c” OPTION
do
    case $OPTION in
        c)
            print_blue "Compiling"
            COMPILE=true
             ;;
        ?)
             echo "fail"
             exit
             ;;
     esac
done

if [ $1 ] && [ $1 != '-c' ] ; then
    print_blue "Only on app $1"
    translate $1
elif [ $2 ] && [ $2 != '-c' ] ; then
    print_blue "Only on app $2"
    translate $2
else
    translate "base"
    translate "users"
    translate "regions"
    translate "parameters"
fi
