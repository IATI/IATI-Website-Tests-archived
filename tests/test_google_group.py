import pytest
from web_test_base import *

class TestGoogleGroup(WebTestBase):
    requests_to_load = {
        'Google Group Landing Page': {
            'url': 'https://groups.google.com/forum/#!forum/iati-technical'
        }
    }

    def test_locate_links(self, loaded_request):
        """
        Tests that a page contains links to the defined URLs.
        This test would ideally check to see whether there is a link to:
            http://discuss.iatistandard.org
        Google Groups, however, is loaded primarily with javascript.
        As such, the link does not exist upon a simple load of the page.
        This functionality could be added later with aSelenium test.
        """
        pass
