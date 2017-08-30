from .base import SeleniumDesktopTestCase, SeleniumMobileTestCase


class FlowTest(SeleniumDesktopTestCase):

    def test_homepage(self):
        """Check if the homepage opens"""

        self.get('/')
        self.assert_status_code('200')
        # Now click somewhere or fill in a form


class MobileFlowTest(SeleniumMobileTestCase, FlowTest):

    """Run the tests on a mobile-like browser"""

    pass
