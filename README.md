# Django Project Template (DPT)

A project template for Django 2.2 in Python 3. This project tries to solve problems or features that commonly appear on Magnet projects. The idea is that you start your project using this code as the base.

Master: [![CircleCI](https://circleci.com/gh/magnet-cl/django-project-template.svg?style=svg)](https://circleci.com/gh/magnet-cl/django-project-template)
Development: [![CircleCI](https://circleci.com/gh/magnet-cl/django-project-template/tree/development.svg?style=svg)](https://circleci.com/gh/magnet-cl/django-project-template/tree/development)

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

Remove the `LICENSE` if your new project does not have an MIT license.

## Dependencies
This project works with:

* Python >= 3.8
* pipenv >= 11.9.0
* Python libraries defined in Pipfile
* Node >= 8.5
* Node packages defined in package.json
* PostgreSQL >= 9.6

## Quickstart
If you are using Ubuntu 16.04/18.04/20.04, `quickstart.sh` installs all
dependencies of the project. It assumes you have Node and npm installed.

* `./quickstart.sh`

Starting with Ubuntu 20.04, the default package for PostgreSQL's adapter
is `python3-psycopg2`, which is the default for `quickstart.sh`.
**If you are using Ubuntu 18.04 or lower, you should explicitly use `python-psycopg`** instead, i.e:

* `./quickstart.sh --postgresql_python_library "python-psycopg2"`

There is no problem if you run `quickstart.sh` more than one time.

## Start new app
Use the custom app template to create your apps:

    python manage.py startapp --template=project/app_template {app_name} --model_name [model_name]

The app template assumes your app name is a plural, the model_name parameter is optional. The template contains the following:

 - A model that is named the same as your app, but in singular. The model name can be changed by passing the model_name parameter to the startapp command.
 - A views.py file with all CRUD views for the model.
 - A urls.py file mapping all CRUD views.
 - A managers.py file with a single QuerySet for the model
 - A forms.py file with a single Form for the model
 - An admin.py file with a single Admin for the model
 - A templates folder with templates in .pug format for all CRUD views.

## Models

### BaseModel

Every model has to inherit from the class BaseModel. This allows that every
model has the fields `created_at` and `updated_at` and methods like `to_json`
and `to_dict`.

### OrderableModel

This model inherits from BaseModel. It adds the `display_order` field to allow
customizable ordering. Change the `set_display_order_` method to change the logic of how a new object is arranged.

## Forms

### BaseModelForm

Every Form has to inherit from this class. It enables fieldset support and changes the style of inputs. For example, date fields will contain a class that is picked up by the datepicker javascript library and render a datepicker input.

If you are handling Chilean RUTs, install [Django Local Flavor](https://github.com/django/django-localflavor).

## Views

Contains classes that inherit from Django generic class based views. This is
done to add new features to this classes, for example
[formset](https://docs.djangoproject.com/en/2.2/topics/forms/formsets/) support.

### 	LoginPermissionRequiredMixin

This clasas inhertis from django's AccessMixin. Verifies that the current user is authenticated (if the attribute login_required is True) and has the required permission (if permission_required is set)

### Clases

### BaseTemplateView

Renders a given template. Inherits from
[TemplateView](https://docs.djangoproject.com/en/2.2/ref/class-based-views/base/#templateview).


### BaseDetailView

Renders a given object. Inherits from
[DetailView](https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#detailview).


### BaseListView

Renders a list of objects. Inherits from
[ListView](https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#listview).


### BaseCreateView

Renders a form to create a single object for a given model. Inherits from [CreateView](https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#createview).


### BaseUpdateView

Renders a form to update a single object of a given model. Inherits from  [UpdateView](https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#updateview).


### BaseDeleteView

Renders a form to delete a single object of a given model. Inherits from [DeleteView](https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#deleteview).


### 	BaseRedirectView

Redirects to a given url. Inherits from
[RedirectView](https://docs.djangoproject.com/en/2.2/ref/class-based-views/base/#redirectview).


### BaseUpdateRedirectView

Redirects to a given url after calling the method `do_action`. Useful when processing something and then redirecting to show the result. Inherits from BaseRedirectView


### StatusView

View that shows internal data of the site, for example if the CAPTCHA is activated or if the site has google analytics.

### FormsetCreateView

View to create an object and a list of child objects with a form and a
[formset](https://docs.djangoproject.com/en/2.2/topics/forms/formsets/).


### FormsetUpdateView

View to updadte an object and a list of child objects with a form and a
[formset](https://docs.djangoproject.com/en/2.2/topics/forms/formsets/).


## Custom apps


### Regions

App with the list for regions and communes of Chile. Both models are populated by migrations.


### Parameters

App to set application wide parameters in the admin.

The parameters are stored in the `Parameter` model and can be retrieved with
`Parameter.value_for(param_name)`. Using this method is recommended since it
uses CACHE (since it is assumed that parameters rarely change).

To set a list Parameters that the app needs with their default values, place
them in `parameters/enums.py`. There is an example with a parameter called
`DEFAULT_URL_PROTOCOL`.

### Users

App that overrides the Django User with the class `User` that is easily modifiable.

### 	API

App that contains the base files to create a REST API with [Django Rest Framework]([https://www.django-rest-framework.org/](https://www.django-rest-framework.org/))

## Pug

The template engine used is pypugjs, a python implementation of the [pugjs](https://pugjs.org/api/getting-started.html) template engine. This converts the pug files into the default templates used in DJango, so you can use both systems on the same template. For example, [variable interpolation in pug](https://pugjs.org/language/interpolation.html) with `#{}`, or using django method with `{{ }}`

Comments are done with  `//-`. If you require HTML comments (visible to final users on the page's source code) use`//`.


### Base template: base.pug
All view templates should extend base.pug, this renders the layout with a navbar and the footer. This templates has the following blocks:

 1. title: Set the content of the title meta tag. By default is set to the `title` variable.
 2. stylesheets: A place to put stylesheets for the given template. By default is empty. Be careful to use this block, it should only be used when the webpack-compiled styles are not enough for some reason.
 3. breadcrumbs: A place to put breadcrumb elements after the `home` element and befor the element that contains the `title`.
 4. content_title: The place to put the `h1` tag. By default contains a `h1` tag with the `title` and a place to put buttons
 5. options: A place to put buttons beside the `h1` tag.
 6. content: The main content of the page. **This should always be defined in the template**
 7. javascripts: A place to put javascripts for the given template. By default is empty. Be careful to use this block, it should only be used when the webpack-compiled javascripts are not enough for some reason.

All these blocks are optional **except content** since they have default implementations.

The navbar template is included base.pug and it can be found in `base/templates/includes/navbar.pug`

The footer template is included base.pug and it can be found in `base/templates/includes/footer.pug`

### Forms

Forms should extend from form.pug (which in turns extends base.pug).

This templates has the following blocks:

 - content_header: A place to put content before the form.
 - top_fields: A place content before the first field defined in the `form` variable.
 - form_fields:  The place that renders the content of the `form` variable.
 - bottom_fields: A place content after the last field defined in the `form` variable.
 - buttons: The place to put the form buttons.
 - submit_button_value: The value of the submit button.
 - submit_button_text: The text of the submit button.
 - cancel_button_url: The url to send the user if the button cancel is pressed. By default is {{cancel_url}}
 - cancel_button_text: Te text of the cancel button.
 - content_footer: The content to be placed after the form.

**All this blocks are optional** since they have default implementations.

If you have chilean RUT input, use the `rut` class too enable javascript validation.

## Test

### Mockups

On `base/mockups.py` there is a class called Mockups, it's a class to create objects for our clases to be used on testing. Every model defined by us requires a method in this class called create_<model_name> if you don't define this method, a test will fail.

### 	BaseTestCase

Base class that all tests clases should inherit from. This class inherits from Django's `TestCase` class and also from the Mockups class. This allow tests that can create their own objects to work with.

## Settings - Local Settings

Since this is a project template, the project folder created by django-admin can't be named after the project itself, that is why it has the generic name `project`.
Within this folder, we can find the `settings.py` file, a typical settings file from Django that also include the following settings>

* Configuration for  Google Analytics y reCAPTCHA
* Santiago/Chile Timezone
* AWS s3 support (deactivated by default)
* Cache with Memcached
* Frontend with Webpack
* Django REST framework in camel case configuration
* Only add debug_toolbar to the INSTALLED_APPS list when debug is True
* Only enable  BrowsableAPIRenderer when debug is True

There are some settings that are not versioned, to that effect we use a not-versioned file (`project/local_settings.py`)  that you have to create. The database configuration, third party service passwords, credentials, etc are placed in this file.

This file is created by `quickstart.sh` if it does not exist by copying  `project/local_settings.py.default`.

To import values from `local_settings` to `settings`, the method get_local_value is used, this allows the existence of optional settings.

## Utils

### Pipenv

We use [Pipenv](https://github.com/pypa/pipenv) to manage Python dependencies.

Instead of running (for example) `pip install localflavor`, use `pipenv install localflavor==1.8`, locking to the version you want (usually the latest, which you can check on [PyPI](https://pypi.org/project/localflavor/#history)).

We set versions to avoid "bugfix" releases breaking our apps. One exception is Django, whose version is specified with `~=` instead of `==`, because its security releases are critical and tend to be done with care.

### Scripts

The script quickstart.sh is used to install all project dependencies and generate the local settings file. If there are dependancies that cannot be installed with pip or npm, then quickstart.sh is the place to install them.

The script reset.sh is used to delete the local database on your computer and create a new one using the django migrations. It's useful to delete trash data when developing or testing your migrations.


### Code

If you need to place methods that are useful to the entire application, place them in `base/utils.py` Some methods that are already included:

 - today: A method that returns the current date in local time (`datetime.date.today` and `timezone.now.date` return the UTC date).
 - date_to_datetime: method that transforms a date into datetime taking into consideration ambiguous or non-existent datetimes due to time changes


## Assets

### Webpack

The project uses `django-webpack-loader` and `webpack` for js, scss and assets with `babel` for es6+ support and `dart-sass` for new features of scss support.
To compile and serve the assets on development, run on separated console:

    npm run start

To generate production bundle run:

    npm run build

### Libraries

Currently there are libraries included "the old fashioned way" on `base/templates/base.pug` using the &lt;script> tag pointint to a CDN. This is done to optimize page load time since the users might have already a copy from the CDN.

The second way to include a library is to use Webpack and NPM. First, install
the library with `npm install` and import it with `import` in the assets file.
The entry point is assets/js/index.js. Note that the same javascript is
executed on all pages, since it's a single bundle. So, to implement different
behaviors, use "components" like if it was React: for example every input that
validate rut, requires the class "rut" that is searched with jQuery.
If there is a behavior unique to a page, use a unique id.

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

### font-awesome
By default the site has a free font awesome 5 kit that uses web fonts.

### Logging Database Entries

The project automatically generates logs for every user action that create, delete or
updates an apps models object. If a field of the object is updated, the log will store
the initial and the final state of the field. The log will ignore the update of the
many2many fields. If a model has a sensitive field for wich you don't want to display
the update information, you have to add it to LOG_SENSITIVE_FIELDS in settings. If you
want to ignore a field, you can add it to LOG_IGNORE_FIELDS in settings.

The project doesn't log any action made through automatic tasks.

## Crons

The project has a dependency installed called
[django-cron](https://github.com/tivix/django-cron) that allows to program
classes that can later be called using the system cron (this means that when
app is deployed, a cron must call django-cron so your classes can be
executed). Every cron job class that you create for your project should
inherit from BaseCronJob in base/cron.py, and should be registered under 
"CRON_CLASSES" in project/settings.py.

There is a class already registered: base.cron.ClearSessionsCronJob. This is a
job that clears expired sessions from the database, everyday at 3:00 am. See the documentation [here](
https://docs.djangoproject.com/en/2.2/topics/http/sessions/#clearing-the-session-store)).


## Deployment

Deployment is automated with Ansible, which is installed by quickstart. Add your servers to `ansible/inventory.yaml` and deploy with:
* `ansible/deploy.sh <host_name>`

After a successful deployment, you can update with:
* `ansible/update.sh <host_name>`

For more information and additional tasks, see `ansible/Readme.md`.
