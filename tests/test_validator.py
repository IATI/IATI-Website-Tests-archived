import pytest
from web_test_base import *

class TestIATIValidator(WebTestBase):
    requests_to_load = {
        'IATI Validator': {
            'url': 'http://validator.iatistandard.org/'
        }
        , 'Valid paste data': {
            'url': 'http://validator.iatistandard.org/index.php'
            , 'method': 'POST'
            , 'data': {
                'paste': utility.load_file_contents('valid.xml')
            }
        }
        , 'Invalid paste data': {
            'url': 'http://validator.iatistandard.org/index.php'
            , 'method': 'POST'
            , 'data': {
                'paste': utility.load_file_contents('invalid.xml')
            }
        }
        , 'Valid URL data': {
            'url': 'http://validator.iatistandard.org/index.php'
            , 'method': 'POST'
            , 'data': {
                'url': 'https://raw.githubusercontent.com/IATI/IATI-Extra-Documentation/version-2.01/en/activity-standard/activity-standard-example-annotated.xml'
            }
        }
        , 'Invalid URL data': {
            'url': 'http://validator.iatistandard.org/index.php'
            , 'method': 'POST'
            , 'data': {
                'url': 'http://validator.iatistandard.org/index.php'
            }
        }
    }

    def test_contains_links(self, loaded_request):
        """
        Test that each page contains links to the defined URLs.
        """
        result = utility.get_links_from_page(loaded_request)

        assert "http://iatistandard.org/" in result

    @pytest.mark.parametrize("target_request", ["IATI Validator"])
    def test_contains_form(self, target_request):
        """
        Test that the validator contains a form on each of three tabs.
        """
        req = self.loaded_request_from_test_name(target_request)

        assert len(utility.locate_xpath_result(req, '//*[@id="status"]/div/form')) == 1
        assert len(utility.locate_xpath_result(req, '//*[@id="fileTab"]/div/form')) == 1
        assert len(utility.locate_xpath_result(req, '//*[@id="extra"]/div/form')) == 1

    @pytest.mark.parametrize("target_request", ["Valid paste data", "Valid URL data"])
    def test_valid_pasted_xml(self, target_request):
        """
        Tests that the validator correctly detects valid XML as valid.
        """
        text_to_find = "This is a well formed xml file."
        xpath_to_locate = '//*[@id="status"]/div[2]'

        assert self.passes_text_detection_test(target_request, text_to_find, xpath_to_locate)

    @pytest.mark.parametrize("target_request", ["Invalid paste data", "Invalid URL data"])
    def test_invalid_pasted_xml(self, target_request):
        """
        Tests that the validator correctly detects invalid XML as invalid.
        """
        text_to_find = "This is not a well-formed xml file"
        xpath_to_locate = '//*[@id="status"]/div[2]'

        assert self.passes_text_detection_test(target_request, text_to_find, xpath_to_locate)
