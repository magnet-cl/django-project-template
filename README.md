# django-project-template-py3
A project template for Django 2.2 in Python 3

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
* pipenv >= 11.9.0
* Python libraries defined in Pipfile
* Node >= 8.5
* Node packages defined in package.json
* PostgreSQL >= 9.6

## Quickstart
If you are using Ubuntu 16.04 or OS X, the script quickstart.sh installs all
dependencies of the project. It assumes you have npm installed.

* `./quickstart.sh`

## Start new app
Use the custom app template to create your apps:

    python manage.py startapp --template=project/app_template answers

## Javascript stuff

on development run on separated console:

    npm run start

for generate production bundle run:

    npm run build

### webpack

The project use `django-webpack-loader` and `webpack` for js, scss and assets with
`babel` for es6+ support and `dart-sass` for new features of scss support.

### Select2

The project comes with select2 by default for all selects. If you wish to
disable this feature add the class .js-not-select2 to the select

### eonasdan-bootstrap-datetimepicker

The project comes with eonasdan-bootstrap-datetimepicker by default for all
inputs that have the .datetime-picker class.

### disable on submit

The project disables all buttons and inputs of submit type
within a form after submit. This is done with a timeout of 10 milliseconds to
avoid not sending values of inputs with type submit. To disable this behaviour, add
.js-do-not-disable-on-submit class to the buttons you don't want to disable.

### chained regions and communes selects

The project comes with chained regions and communes selects.
To able this add regions.js in the regions and communes selects template.

### Rut formatter

The project comes with rut formatter and validation for all inputs with .rut class.
To disable any of this behaviour, add .js-do-not-format-rut or .js-do-not-validate-rut
class to the inputs you don't want to format or validate, respectively.

### App.utils

* App.utils.showLoading(): Shows a spinner on the navbar and puts the cursor
on wait
* App.utils.hideLoading(): Reverts changes caused by showLoading
on wait
* App.utils.thousandSeparator(): for a given number in text, returns the text
with thoushand separators (for spanish)
on wait

### Logging Database Entries

The project generates a LogEntry object for every action of a user that create, delete
or updates an apps model's object. If field is updated the log will store the initial
and final state of the field. The log will not store any modification made to a
many2many field. If the a model has a sensitive field that you don want to show in the
log, you can add it to 'sensitive_fields' in base/signals.py.
The project doesn't log any action made through automatic tasks.
