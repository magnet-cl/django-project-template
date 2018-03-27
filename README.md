# django-project-template-py3
A project template for Django 1.11 in Python 3

[![CircleCI](https://circleci.com/gh/magnet-cl/django-project-template-py3.svg?style=svg)](https://circleci.com/gh/magnet-cl/django-project-template-py3)
[![CircleCI](https://circleci.com/gh/magnet-cl/django-project-template-py3/tree/testing.svg?style=svg)](https://circleci.com/gh/magnet-cl/django-project-template-py3/tree/testing)
[![CircleCI](https://circleci.com/gh/magnet-cl/django-project-template-py3/tree/development.svg?style=svg)](https://circleci.com/gh/magnet-cl/django-project-template-py3/tree/development)

## Get the code
Create a new repository for your django project and clone your repository into
your computer.

Add the django-project-template-py3 github repo as a remote repository:
* `git remote add template
  git@github.com:magnet-cl/django-project-template-py3.git`

Pull the code from the project template:
* `git pull template master`

Push to your own repo
* `git push origin master`

Now you have your own django project in your repository.

## Dependencies
This project works with:

* Python >= 3.6
* Python libraries defined in requirements.txt 
* Node >= 8.5
* Node libraries defined in package.json 
* Postgress >= 9.6 

## Quickstart
If you are using Ubuntu 16.04 or OSX, the script quickstart.sh installs all 
dependencies of the project. It assumes you have yarn installed.

* `./quickstart.sh`

## Start new app
Use the custom app template to create your apps:

    python manage.py startapp --template=project/app_template answers

## Javascript stuff

### Select2

The project comes with select2 by default for all selects. If you wish to
disable this feature add the class .js-not-select2 to the selec

### eonasdan-bootstrap-datetimepicker

The project comes with eonasdan-bootstrap-datetimepicker by default for all
inputs that have the .datetime-picker class.

### disable on submit

The project disables all buttons and inputs of submit type
within a form after submit. This is done with a timeout of 10 milliseconds to
avoid not sending values of inputs with type submit. To disable this behaviour, add
.js-do-not-disable-on-submit class to the buttons you don't want to disable.


### App.utils

* App.utils.showLoading(): Shows a spinner on the navbar and puts the cursor
on wait
* App.utils.hideLoading(): Reverts changes caused by showLoading
on wait
* App.utils.thousandSeparator(): for a given number in text, returns the text
with thoushand separators (for spanish)
on wait
