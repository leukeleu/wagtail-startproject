from .base import SeleniumTestCase


class FlowTest(SeleniumTestCase):

    def test_homepage(self):
        """Check if the homepage opens"""

        self.get('/')
        self.assert_status_code('200')
        # Now click somewhere or fill in a form
