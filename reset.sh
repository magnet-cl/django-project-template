#!/bin/bash

RUNSERVER=false
while getopts “sh” OPTION
do
    case $OPTION in
        s)
             echo "Start Server"
             RUNSERVER=true
             ;;
        ?)
             echo "fail"
             exit
             ;;
     esac
done

engine=`python -c"from project.settings import LOCAL_DATABASES; print(LOCAL_DATABASES['default']['ENGINE'])"`
debug=`python -c"from project.settings import LOCAL_DEBUG; print(LOCAL_DEBUG)"`
dbname=`python -c"from project.settings import LOCAL_DATABASES; print(LOCAL_DATABASES['default']['NAME'])"`

if [ $debug = "True" ] ; then
echo "----------------------drop-database------------------------------"
    if [ $engine == "django.db.backends.sqlite3" ]; then
        if [ -f $dbname ] ; then
            echo "SQLITE: deleting $dbname"
            rm $dbname
        fi
    else
        dbuser=`python -c"from project.settings import LOCAL_DATABASES; print(LOCAL_DATABASES['default']['USER'])"`
        dbpass=`python -c"from project.settings import LOCAL_DATABASES; print(LOCAL_DATABASES['default']['PASSWORD'])"`
        if [ $engine == "django.db.backends.mysql" ]; then
            echo "drop database $dbname" | mysql --user=$dbuser --password=$dbpass
            echo "create database $dbname" | mysql --user=$dbuser --password=$dbpass
        else
            dropdb $dbname
            createdb $dbname
        fi
    fi
    python manage.py migrate
fi

if  $RUNSERVER ; then
    python manage.py runserver 0.0.0.0:8000 --nothreading
fi
