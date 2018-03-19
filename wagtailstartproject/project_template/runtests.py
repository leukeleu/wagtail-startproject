#!/usr/bin/env python
import argparse
import os
import sys

import django

from django.conf import settings
from django.test.runner import default_test_processes
from django.test.utils import get_runner


def runtests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()

    if args.headful:
        settings.HEADLESS = False

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
        '--parallel',
        type=int,
        nargs='?',
        const=default_test_processes(),  # arg is given without value
        default=1,  # arg is not given
        help='do run multiple tests in parallel (how many if specified, else as many as possible)'
    )
    parser.add_argument(
        '--headful',
        action='store_true',
        help='do not run headless (checkout tests running onscreen)'
    )

    args = parser.parse_args()
    runtests()
