import pytest
from web_test_base import *

class TestIATIWiki(WebTestBase):
    requests_to_load = {
        'IATI Wiki Homepage': {
            'url': 'http://wiki.archive.iatistandard.org/'
        }
    }

    def test_locate_links(self, loaded_request):
        """
        Tests that each page contains links to the defined URLs.
        """
        result = utility.get_links_from_page(loaded_request)

        assert "http://www.iatistandard.org" in result
        assert "http://www.iatiregistry.org" in result
