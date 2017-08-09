from wagtail.wagtailcore.models import Page

from .base import SeleniumDesktopTestCase


class PagesTest(SeleniumDesktopTestCase):

    def test_wagtail_pages(self):
        """Check if all Wagtail pages can be retrieved"""

        pages = Page.objects.live()
        for page in pages:
            url = page.relative_url(page.get_site())
            if url is not None:
                self.get(url)
                self.assert_status_code('200')
