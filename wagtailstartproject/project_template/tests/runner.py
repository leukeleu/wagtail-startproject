import os
import subprocess

from django.core.management import call_command
from django.db import connections
from django.conf import settings

try:
    import tblib.pickling_support
except ImportError:
    tblib = None
from django.test.runner import DiscoverRunner, get_unique_databases_and_mirrors


class KeepDBRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        test_databases, mirrored_aliases = get_unique_databases_and_mirrors()

        old_names = []

        for signature, (db_name, aliases) in test_databases.items():
            first_alias = None
            for alias in aliases:
                connection = connections[alias]
                old_names.append((connection, db_name, first_alias is None))

                # Actually create the database for the first connection
                if first_alias is None:
                    first_alias = alias

                    connection_creation = connection.creation
                    test_database_name = connection_creation._get_test_db_name()

                    #create the database
                    connection_creation._create_test_db(
                        verbosity=self.verbosity,
                        autoclobber=not self.interactive,
                        keepdb=self.keepdb,
                    )
                    connection_creation.connection.close()
                    settings.DATABASES[connection_creation.connection.alias]["NAME"] = test_database_name
                    connection_creation.connection.settings_dict["NAME"] = test_database_name

                    # Create the tables using to the SQL dump
                    FNULL = open(os.devnull, 'w')
                    # using psql because we do a full restore anyways
                    # https://www.postgresql.org/message-id/NEBBLAAHGLEEPCGOBHDGAECGHEAA.nickf%40ontko.com
                    subprocess.call([
                            'psql',
                            '{dbname}'.format(dbname=settings.DATABASES.get('default').get('TEST').get('NAME')),
                            '--file={dir}{sqldump_path}'.format(
                                dir=settings.FIXTURE_DIRS[0],
                                sqldump_path='basic_site.sql',
                            )
                        ],
                        stdout=FNULL
                    )

                    # Only run the migrations that are newer than what the original database knows about
                    call_command(
                        'migrate',
                        verbosity=max(self.verbosity - 1, 0),
                        interactive=False,
                        database=connection_creation.connection.alias,
                        run_syncdb=True,
                    )

                    if self.parallel > 1:
                        for index in range(self.parallel):
                            connection.creation.clone_test_db(
                                number=index + 1,
                                verbosity=self.verbosity,
                                keepdb=self.keepdb,
                            )
                # Configure all other connections as mirrors of the first one
                else:
                    connections[alias].creation.set_as_test_mirror(
                        connections[first_alias].settings_dict)

        # Configure the test mirrors.
        for alias, mirror_alias in mirrored_aliases.items():
            connections[alias].creation.set_as_test_mirror(
                connections[mirror_alias].settings_dict)

        if self.debug_sql:
            for alias in connections:
                connections[alias].force_debug_cursor = True

        return old_names