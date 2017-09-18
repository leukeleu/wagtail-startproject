import os
import subprocess

from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.db import transaction


class FakeException(Exception):
    pass


class Command(BaseCommand):
    help = "Create a fixture for Selenium tests"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        """Perform data manipulation and datadump without affecting the database"""
        try:
            with transaction.atomic():
                self.manipulate_data()
                self.create_fixture()
                raise FakeException('Trigger rollback')
        except FakeException:
            pass

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

        json_path = os.path.join(settings.BASE_DIR, 'tests/fixtures/basic_site.json')
        sql_path = os.path.join(settings.BASE_DIR, 'tests/fixtures/basic_site.sql')

        call_command(
            'dumpdata',
            exclude=excluded,
            natural_foreign=True,
            indent=2,
            output=json_path
        )

        # TODO: find a way to have it anonymized
        subprocess.call(
            [
                'pg_dump',
                '--no-owner',
                '--no-privileges',
                '--file={file}'.format(file=sql_path),
                '{dbname}'.format(dbname=settings.DATABASES.get('default').get('NAME')),
            ]
        )
