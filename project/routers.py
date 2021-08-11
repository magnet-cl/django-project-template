# django
from django.conf import settings
from django.db import DatabaseError


class DatabaseByAppRouter:
    """
    A router to control all database operations on models and applications.

    https://docs.djangoproject.com/en/2.2/topics/db/multi-db/#automatic-database-routing

    Example:

        DATABASE_BY_APPS = {
            'logs': [
                'regions',  # by application
                'regions.Commune',  # by model
            ],
        }
    """

    DEFAULT_DATABASE = 'default'

    def __init__(self):
        databases = settings.DATABASES.keys()
        database_by_apps = settings.DATABASE_BY_APPS

        # validate if exists selected database on database by apps
        for database in database_by_apps.keys():
            if database not in databases:
                raise DatabaseError(
                    f'Connection to database "{database}" not found'
                    ' on database by apps.'
                )

        self.app_databases = {}
        for database, applications in database_by_apps.items():
            for app in applications:
                # set applications or model
                self.app_databases[app] = database

    def get_database_name(self, app_label, model_name):
        """
        Return database name by models or apps
        """
        return self.app_databases.get(
            # get database by model
            f'{app_label}.{str(model_name).title()}',
            # get database by app
            self.app_databases.get(app_label, self.DEFAULT_DATABASE)
        )

    def get_database_name_from_model(self, model):
        """
        Return database name by models
        """
        app_label = model._meta.app_label
        model_name = model.__name__
        return self.get_database_name(app_label, model_name)

    def db_for_read(self, model, **hints):
        """
        Attempts to read models from database.
        """
        return self.get_database_name_from_model(model)

    def db_for_write(self, model, **hints):
        """
        Attempts to write models from database.
        """
        return self.get_database_name_from_model(model)

    def allow_relation(self, obj1, obj2, **hints) -> bool:
        """
        Keeps relations on same database.

        Returns: bool
        """
        return (
            self.get_database_name_from_model(obj1.__class__) ==
            self.get_database_name_from_model(obj2.__class__)
        )

    def allow_migrate(self, db, app_label, model_name=None, **hints) -> bool:
        """
        Make sure apps only appear in selected database.

        Returns: bool
            True:
                Model is created on current database

            False:
                Model isn't created on current database

        """
        if model := hints.get('model', None):
            # for historical models
            return db == self.get_database_name_from_model(model)
        else:
            return db == self.get_database_name(app_label, model_name)
