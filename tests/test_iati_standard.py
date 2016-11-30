import re
import pytest
from web_test_base import *

class TestIATIStandard(WebTestBase):
    requests_to_load = {
        'IATI Standard Homepage - no www': {
            'url': 'http://iatistandard.org/'
        }
        , 'IATI Standard Homepage - with www': {
            'url': 'http://www.iatistandard.org/'
        }
        , 'IATI Standard - Misc Guidance Page': {
            'url': 'http://iatistandard.org/202/guidance/how-to-publish/prepare-your-org/'
        }
        , 'IATI Standard - Summary Page': {
            'url': 'http://iatistandard.org/202/organisation-standard/summary-table/'
        }
        , 'IATI Standard - Schema Page': {
            'url': 'http://iatistandard.org/202/schema/'
        }
        , 'IATI Standard - Old Schema Version, Developer Docs': {
            'url': 'http://iatistandard.org/105/developer/'
        }
        , 'IATI Standard - Misc Developer Docs Page': {
            'url': 'http://iatistandard.org/105/developer/xquery/'
        }
        , 'IATI Standard - Activity Standard Docs Page': {
            'url': 'http://iatistandard.org/105/activity-standard/iati-activities/iati-activity/contact-info/'
        }
        , 'IATI Standard - Schema Version Homepage': {
            'url': 'http://iatistandard.org/201/'
        }
    }

    def test_locate_links(self, loaded_request):
        """
        Tests that each page contains links to the defined URLs.
        """
        result = utility.get_links_from_page(loaded_request)

        assert "http://iatistandard.org" in result
        assert "http://www.aidtransparency.net/" in result
        assert "http://iatiregistry.org" in result
        assert utility.regex_match_in_list('^(\.\./)*license/$', result)
        assert "http://glyphicons.com" in result
        assert "http://creativecommons.org/licenses/by/3.0/" in result

    def test_footer_license_information(self, loaded_request):
        """
        Tests that the footer contains license information.
        This should include information about each text and icon licensing.
        """
        footer_xpath = '//*[@id="footer-credits"]/span'

        result = utility.get_text_from_xpath(loaded_request, footer_xpath)

        assert utility.substring_in_list('Text licensed under CC BY 4.0', result)
