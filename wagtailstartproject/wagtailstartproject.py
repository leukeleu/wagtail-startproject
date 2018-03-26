#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

import os

from argparse import ArgumentParser
from keyword import iskeyword

from django.core.management import ManagementUtility


def check_project_name(parser, project_name):
    """Perform checks for the given project name.

    Checks:
    - not a reserved Python keyword.
    - not already in use by another Python package/module.

    """
    if iskeyword(project_name):
        parser.error("'{project_name}' can not be a reserved Python keyword.".format(project_name=project_name))

    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        parser.error("'{project_name}' conflicts with the name of an existing "
                     "Python module and cannot be used as a project "
                     "name. Please try another name.".format(project_name=project_name))


def create_project(project_name):
    """Create the project using the Django startproject command"""

    print("Creating a Wagtail project called {project_name}".format(project_name=project_name))

    import wagtailstartproject
    wagtailstartproject_path = os.path.dirname(wagtailstartproject.__file__)

    template_path = os.path.join(wagtailstartproject_path, 'project_template')

    # Call django-admin startproject
    # https://docs.djangoproject.com/en/2.0/ref/django-admin/#startproject
    utility_args = [
        'django-admin.py',
        'startproject',
        '--template=' + template_path,
        '--extension=py,ini,html,rst,json,cfg',
        '--name=Makefile',
        project_name
    ]

    # always put the project template inside the current directory:
    utility_args.append('.')

    utility = ManagementUtility(utility_args)
    utility.execute()

    print("Success! {project_name} has been created".format(project_name=project_name))


def main():
    parser = ArgumentParser(description="Setup a project for a new wagtail based website inside the current directory")
    parser.add_argument('project_name', help="name of the project to create")
    args = parser.parse_args()

    check_project_name(parser, args.project_name)

    create_project(args.project_name)


if __name__ == "__main__":
    main()
