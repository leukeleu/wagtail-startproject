import unittest

from itertools import chain
from os import environ, path, rmdir
from tempfile import mkdtemp
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import Resolver404, resolve
from django.test.runner import RemoteTestResult


class SeleniumTestCase(StaticLiveServerTestCase):

    """
    Tests with a Selenium webdriver to run tests in a browser.

    Defaults to the Chrome browser.

    """

    fixtures = ['basic_site.json']

    @classmethod
    def setUpClass(cls):
        """Start the webrdriver and create a temp dir to store screenshots of failed tests"""

        super(SeleniumTestCase, cls).setUpClass()
        cls.driver = cls.get_driver()
        cls.screenshot_dir = mkdtemp()

    @classmethod
    def tearDownClass(cls):
        """Quit the browser and print screenshot dir location if it contains screenshots"""

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
    def get_driver(cls):
        """Setup a Chrome webdriver"""

        options = webdriver.ChromeOptions()
        options.set_headless(headless=getattr(settings, 'HEADLESS', True))
        cls.set_driver_options(options)
        try:
            driver = webdriver.Chrome('./node_modules/.bin/chromedriver', chrome_options=options)
        except WebDriverException:
            raise unittest.SkipTest('Not able to start Chrome driver.')
        return driver

    @classmethod
    def set_driver_options(cls, options):
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
        """Wait until the given test element is gone"""

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
    def set_driver_options(cls, options):
        options.add_argument('window-size=1200,900')

    def wait_for_form_submit(self):
        """Use after submitting a form"""
        pass


class SeleniumMobileTestCase(SeleniumTestCase):

    """Selenium tests with a mobile-sized browser"""

    @classmethod
    def set_driver_options(cls, options):
        options.add_experimental_option('mobileEmulation', {"deviceName": "iPhone 5"})


class FirefoxDriverMixin(object):

    @classmethod
    def get_driver(cls):
        """Setup a Firefox webdriver"""

        environ['MOZ_HEADLESS'] = "1"
        options = webdriver.firefox.options.Options()
        cls.set_driver_options(options)
        options.set_headless(headless=getattr(settings, 'HEADLESS', True))
        try:
            driver = webdriver.Firefox(executable_path='./node_modules/.bin/geckodriver', firefox_options=options)
        except WebDriverException:
            raise unittest.SkipTest('Not able to start Firefox driver.')
        driver.set_window_size(1200, 900)
        return driver

    @classmethod
    def set_driver_options(cls, options):
        pass

    def wait_for_form_submit(self):
        """Use after submitting a form"""
        sleep(2)
