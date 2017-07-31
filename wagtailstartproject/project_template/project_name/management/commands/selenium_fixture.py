import os

from django.core.management import BaseCommand, call_command
from django.conf import settings
from django.db import transaction


class Command(BaseCommand):
    help = "Create a fixture for Selenium tests"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):

        try:
            with transaction.atomic():
                self.manipulate_data()
                self.create_fixture()
        except:

        raise ValueError('Transaction needed to be rolled back, but everything went fine!')

    def manipulate_data(self):
        """Make changes to the data in the database before dumping

        These changes will be reverted (transaction) after the fixture is created.

        """
        pass

    def create_fixture(self):
        """Create the fixture using the dumpdata command"""

        excluded = [
            'admin',
            'auth.Permission',
            'contenttypes',
            'sessions',
            'wagtailcore.grouppagepermission',
            'wagtailcore.groupcollectionpermission',
        ]

        path = os.path.join(settings.BASE_DIR, 'tests/fixtures/basic_site.json')

        call_command(
            'dumpdata',
            exclude=excluded,
            natural_foreign=True,
            indent=2,
            output=path
        )
