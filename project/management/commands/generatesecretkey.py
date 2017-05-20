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

        file_path = "{}/settings.py".format(settings.PROJECT_DIR)

        for line in fileinput.input(file_path, inplace=True):
            if line.startswith("SECRET_KEY = "):
                print("SECRET_KEY = '{}'".format(secret_key))
            else:
                print(line, end='')
