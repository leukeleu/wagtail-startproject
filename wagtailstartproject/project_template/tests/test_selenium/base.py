import unittest

from itertools import chain
from os import path, rmdir
from tempfile import mkdtemp

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import Resolver404, resolve
from django.test.runner import RemoteTestResult


class SeleniumTestCase(StaticLiveServerTestCase):
    fixtures = ['basic_site.json']

    @classmethod
    def setUpClass(cls):
        super(SeleniumTestCase, cls).setUpClass()
        # Every test needs a Chrome driver.
        try:
            cls.driver = cls.get_chrome_driver()
        except WebDriverException:
            raise unittest.SkipTest('Not able to start Chrome driver.')
        # Create temp dir to store screenshots of failed tests
        cls.screenshot_dir = mkdtemp()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        try:
            rmdir(cls.screenshot_dir)
        except OSError:
            print
            print('Screenshots of failed tests are stored in:')
            print(cls.screenshot_dir)
        super(SeleniumTestCase, cls).tearDownClass()

    def setUp(self):
        # Allow JS a bit of time to execute
        self.driver.implicitly_wait(3)
        # Navigate to blank to prevent scroll position of previous test to affect this test
        self.get('about:blank')

    def tearDown(self):
        # Reset wait to default
        self.driver.implicitly_wait(0)

        # Take screenshots of final state for failed tests
        result = self._resultForDoCleanups
        try:
            if isinstance(result, RemoteTestResult):
                # When running parallel tests
                current_test_index = next(event[1] for event in reversed(result.events) if event[0] == 'startTest')
                failed = next(True for event in result.events if event[0] in ['addError', 'addFailure'] and event[1] is current_test_index)
            else:
                failed = next(True for method, reason in chain(result.errors, result.failures) if method is self and reason)
        except StopIteration:
            failed = False

        if failed:
            screenshot_path = path.join(self.screenshot_dir, 'screenshot_{test_id}.png'.format(test_id=self.id()))
            self.driver.save_screenshot(screenshot_path)

        super(SeleniumTestCase, self).tearDown()

    @classmethod
    def get_chrome_driver(cls):
        """Setup a Chrome driver"""

        options = webdriver.ChromeOptions()
        cls.get_driver_options()
        options.add_argument('headless')
        driver = webdriver.Chrome('./node_modules/.bin/chromedriver', chrome_options=options)
        return driver

    @classmethod
    def get_driver_options(cls, options):
        """To be overwritten in subclasses with specific options"""
        pass

    def url(self, absolute_url):
        """Prepend the absolute url with the test server url"""

        return '%s%s' % (self.live_server_url, absolute_url)

    def get(self, absolute_url):
        """Use this to navigate to pages

        The absolute_url should be either:
        - a fixed url, e.g. '/contact/'
        - object urls, e.g. page.get_absolute_url()
        - a named url, e.g. reverse('search')

        """
        return self.driver.get(self.url(absolute_url))

    def wait_for_staleness(self, test_element, timeout=3):
        """Wait untill the given test element is gone"""

        WebDriverWait(self.driver, timeout).until(staleness_of(test_element))

    def assert_status_code(self, status_code='200'):
        """Check that the current page has the expected status code

        :param status_code: the status code as string, e.g. '200'.

        """
        meta = self.driver.find_element_by_css_selector('meta[name="status_code"]')
        self.assertEqual(status_code, meta.get_attribute('content'),
                         msg="Unexpected status code for URL: {}".format(self.driver.current_url))

    def assert_model_resolves_expected_view(self, obj, expected_view):
        """Check if expected view is called for the given obj's absolute_url

        In some cases an earlier defined url in the urls.py catches the request.
        For class-based views give function returned by `as_view()` as expected_view.

        """
        url = obj.get_absolute_url()

        try:
            view, args, kwargs = resolve(url)
        except Resolver404:
            raise AssertionError('Unable to resolve the url for the object: "{url}"'.format(url=url))

        self.assertEqual(
            expected_view,
            view,
            msg="Url resolves to {view} instead of the expected {expected_view}.".format(view=view, expected_view=expected_view)
        )


class SeleniumDesktopTestCase(SeleniumTestCase):

    """Selenium tests with a desktop-sized browser"""

    @classmethod
    def get_driver_options(cls, options):
        options.add_argument('window-size=1200,900')


class SeleniumMobileTestCase(SeleniumTestCase):

    """Selenium tests with a mobile-sized browser"""

    @classmethod
    def get_driver_options(cls, options):
        options.add_experimental_option('mobileEmulation', {"deviceName": "iPhone 5"})
