import pytest
from web_test_base import *

class TestAidinfolabsCSVConverter(WebTestBase):
    requests_to_load = {
        'AidInfo Labs CSV Conversion Tool': {
            'url': 'http://tools.aidinfolabs.org/csv/direct_from_registry/'
        }
        , 'Download Valid CSV': {
            'url': 'http://tools.aidinfolabs.org/csv/direct_from_registry/?search=&xml=https%3A%2F%2Fraw.githubusercontent.com%2FIATI%2FIATI-Extra-Documentation%2Fversion-2.01%2Fen%2Factivity-standard%2Factivity-standard-example-annotated.xml&download=true&id=Custom&format=full'
        }
    }

    @pytest.mark.parametrize("target_request", ["AidInfo Labs CSV Conversion Tool"])
    def test_locate_links(self, target_request):
        """
        Tests that a page contains links to the defined URLs.
        """
        loaded_request = self.loaded_request_from_test_name(target_request)

        result = utility.get_links_from_page(loaded_request)

        assert "http://www.iatistandard.org" in result
