# django-project-template
A project template for Django 2.2 in Python 3

[![CircleCI](https://circleci.com/gh/magnet-cl/django-project-template.svg?style=svg)](https://circleci.com/gh/magnet-cl/django-project-template)
[![CircleCI](https://circleci.com/gh/magnet-cl/django-project-template/tree/testing.svg?style=svg)](https://circleci.com/gh/magnet-cl/django-project-template/tree/testing)
[![CircleCI](https://circleci.com/gh/magnet-cl/django-project-template/tree/development.svg?style=svg)](https://circleci.com/gh/magnet-cl/django-project-template/tree/development)

## Get the code
Create a new repository for your django project and clone your repository into
your computer.

Add the django-project-template github repo as a remote repository:
* `git remote add template
  git@github.com:magnet-cl/django-project-template.git`

Pull the code from the project template:
* `git pull template master`

Configure `project_name` and `server_git_url`:
* `vim ansible/group_vars/all.yaml`

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
If you are using Ubuntu 16.04/18.04 or OS X, the script `quickstart.sh` installs all
dependencies of the project. It assumes you have Node and npm installed.

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

### tempusdominus-bootstrap-4

The project comes with [Tempus Dominus Bootstrap 4](https://tempusdominus.github.io/bootstrap-4/) by default for all inputs that have the `.datetimepicker-input` class.

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

The project automatically generates logs for every user action that create, delete or
updates an apps models object. If a field of the object is updated, the log will store
the initial and the final state of the field. The log will ignore the update of the
many2many fields. If a model has a sensitive field for wich you don't want to display
the update information, you have to add it to LOG_SENSITIVE_FIELDS in settings. If you
want to ignore a field, you can add it to LOG_IGNORE_FIELDS in settings.

The project doesn't log any action made through automatic tasks.
## Deployment

Deployment is automated with Ansible, which is installed by quickstart. Add your servers to `ansible/inventory.yaml` and deploy with:
* `ansible/deploy.sh <host_name>`

After a successful deployment, you can update with:
* `ansible/update.sh <host_name>`

For more information and additional tasks, see `ansible/Readme.md`.
