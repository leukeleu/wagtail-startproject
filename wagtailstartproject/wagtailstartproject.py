#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

import os
from optparse import OptionParser

from django.core.management import ManagementUtility


def create_project(parser, options, arguments):
    # Validate args
    if len(arguments) < 1:
        parser.error("Please specify a name for your Wagtail installation")
    elif len(arguments) > 1:
        parser.error("Too many arguments")

    project_name = arguments[0]

    # Make sure given name is not already in use by another python package/module.
    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        parser.error("'%s' conflicts with the name of an existing "
                     "Python module and cannot be used as a project "
                     "name. Please try another name." % project_name)

    print("Creating a Wagtail project called %(project_name)s" % {'project_name': project_name})  # noqa

    # Create the project from the Wagtail template using startapp

    # First find the path to Wagtail
    import wagtailstartproject
    wagtail_path = os.path.dirname(wagtailstartproject.__file__)
    template_path = os.path.join(wagtail_path, 'project_template')
    print(template_path)

    # Call django-admin startproject
    utility_args = ['django-admin.py',
                    'startproject',
                    '--template=' + template_path,
                    '--ext=html,rst',
                    project_name]

    # always put the project template inside the current directory:
    utility_args.append('.')

    utility = ManagementUtility(utility_args)
    utility.execute()

    print("Success! %(project_name)s has been created" % {'project_name': project_name})  # noqa


COMMANDS = {
    'start': create_project,
}


def main():
    # Parse options
    parser = OptionParser(usage="Usage: %prog project_name")
    (options, arguments) = parser.parse_args()

    create_project(parser, options, arguments)

if __name__ == "__main__":
    main()
