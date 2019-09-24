#!/bin/bash
set -e

function print_red() {
    echo -e "\033[31m$1\033[39m"
}

debug=$(python -c "from project.settings import DEBUG; print(DEBUG)")
dbname=$(python -c "from project.settings import LOCAL_DATABASES; print(LOCAL_DATABASES['default']['NAME'])")

if [ "$debug" != "True" ] ; then
  print_red "DEBUG is not True."
  exit 1
fi

echo "----------------------drop-database------------------------------"
dropdb "$dbname"

echo "  create-database"
createdb "$dbname"

python manage.py migrate
