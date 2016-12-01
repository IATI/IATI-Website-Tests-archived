import pytest

from web_test_base import *

"""
A class to test new features without running all of the tests.

Usage:
    py.test tests/test_test.py -rsx
"""
class TestTest(WebTestBase):
    requests_to_load = {
        'implicit GET': {
            'url': 'http://iatistandard.org/'
        }
        , 'explicit GET': {
            'url': 'http://iatistandard.org/202/namespaces-extensions/'
            , 'method': 'GET'
        }
    }

    @pytest.mark.parametrize("target_request", ["implicit GET"])
    def test_locate_text(self, target_request):
        """
        Tests that each page contains the specified text at the required location.
        """
        req = self.loaded_request_from_test_name(target_request)
        text_to_find = "technical publishing framework"
        xpath_to_locate = '//*[@id="home-strapline"]/h1'

        result = utility.get_text_from_xpath(req, xpath_to_locate)

        assert utility.substring_in_list(text_to_find, result)
