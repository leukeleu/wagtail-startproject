from ..test_selenium import test_flow
from ..test_selenium.base import FirefoxDriverMixin


class FirefoxFlowTest(FirefoxDriverMixin, test_flow.FlowTest):

    """Run the tests in the Firefox browser"""

    pass
