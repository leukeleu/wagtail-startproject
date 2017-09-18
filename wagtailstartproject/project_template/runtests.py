#!/usr/bin/env python
import argparse
import os
import sys

import django

from django.conf import settings
from django.test.utils import get_runner


def runtests(args):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()

    if args.sql:
        settings.TEST_RUNNER = 'tests.runner.KeepDBRunner'

    test_runner = get_runner(settings)
    failures = test_runner(parallel=args.parallel).run_tests(args.tests)
    sys.exit(bool(failures))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests')
    parser.add_argument(
        dest='tests',
        metavar='testcase',
        nargs='*',
        default=['tests'],
        help='an optional list of test cases to run'
    )
    parser.add_argument(
        '--sql',
        action='store_true',
        help='load an sql file and ignore the json fixtures during the tests'
    )
    parser.add_argument(
        '--parallel',
        action='store_true',
        help='run multiple tests in parallel'
    )

    args = parser.parse_args()
    runtests(args)
