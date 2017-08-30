{{ project_name }}
======================


Running tests
-------------

Setup for Selenium
~~~~~~~~~~~~~~~~~~

The Selenium tests run in Chrome, this should be installed on a default
location of your OS (e.g. on a Mac in `~/Applications/`). Additionally the
chromedriver needs to be installed. This is easily done using yarn, by
simply installing the devDependencies listed in the package.json.


Run a subset of tests
~~~~~~~~~~~~~~~~~~~~~

To run a specific test call the runtests.py with the path to the desired
test or TestCase, for example::

    ./runtests.py tests.test_selenium.test_flow.MobileFlowTest.test_homepage
