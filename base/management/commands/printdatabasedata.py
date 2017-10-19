from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('setting', nargs='?', type=str)

    def handle(self, *args, **options):
        """ Prints the default database name """
        if options['setting']:
            setting = options.get('setting')
        else:
            setting = 'NAME'

        self.stdout.write(settings.DATABASES['default'][setting])
