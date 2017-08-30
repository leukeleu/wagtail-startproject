try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class PageStatusMiddleware(MiddlewareMixin):
    """Add the response status code as a meta tag in the head of all pages

    Note: Only enable this middleware for (Selenium) tests

    """

    def process_response(self, request, response):
        # Only do this for HTML pages
        # (expecting response['Content-Type'] to be ~ 'text/html; charset=utf-8')
        if 'html' in response['Content-Type'].lower():
            response.content = response.content.replace(
                '</head>',
                '<meta name="status_code" content="{status_code}" /></head>'.format(status_code=response.status_code),
                1
            )

        return response
