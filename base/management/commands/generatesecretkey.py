from django.core.management.templates import BaseCommand
from django.utils.crypto import get_random_string

import fileinput

from django.conf import settings


class Command(BaseCommand):
    help = ("Replaces the SECRET_KEY VALUE in settings.py with a new one.")

    def handle(self, *args, **options):
        # Create a random SECRET_KEY hash to put it in the main settings.
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(50, chars)

        file_path = "{}/local_settings.py".format(settings.PROJECT_DIR)

        line_found = False

        for line in fileinput.input(file_path, inplace=True):
            if line.startswith("SECRET_KEY = "):
                print("SECRET_KEY = '{}'".format(secret_key))
                line_found = True
            else:
                print(line, end='')

        if not line_found:
            with open(file_path, "a") as myfile:
                myfile.write("SECRET_KEY = '{}'".format(secret_key))
