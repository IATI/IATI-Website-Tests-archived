from web_test_base import *

class TestIATIStandard(WebTestBase):
    """
    TODO: Add tests to assert that:
    - the number of activities and publishers roughly matches those displayed on the Registry
    - a key string appears on the homepage
    """
    requests_to_load = {
        'IATI Standard Homepage - no www': {
            'url': 'http://iatistandard.org'
        },
        'IATI Standard Homepage - with www': {
            'url': 'http://www.iatistandard.org'
        }
    }

    def test_contains_links(self, loaded_request):
        """
        Test that each page contains links to the defined URLs.
        """
        result = utility.get_links_from_page(loaded_request)

        # Selection of header links
        assert "/en/news/" in result
        assert "/en/about/" in result
        assert "/en/iati-standard/" in result
        assert "/en/using-data/" in result

        # Selection of footer links
        assert "/en/contact/" in result
        assert "/en/terms-and-conditions/" in result
        assert "/en/privacy-policy/" in result

    def test_contains_newsletter_signup_form(self, loaded_request):
        """
        Tests to confirm that there is always a form to subscribe to the newsletter within the footer.
        """
        xpath = '//*[@id="mc-embedded-subscribe-form"]'

        result = utility.locate_xpath_result(loaded_request, xpath)

        assert len(result) == 1
