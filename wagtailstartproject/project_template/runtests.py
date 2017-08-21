#!/usr/bin/env python
import os
import sys

import django

from django.conf import settings
from django.test.runner import default_test_processes
from django.test.utils import get_runner


def runtests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    test_runner = get_runner(settings)
    if sys.argv[0] != 'setup.py' and len(sys.argv) > 1:
        tests = sys.argv[1:]
    else:
        tests = ['tests']
    failures = test_runner(parallel=default_test_processes()).run_tests(tests)
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
