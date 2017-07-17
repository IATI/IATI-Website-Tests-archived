import pytest
from web_test_base import *

class TestIATIDiscuss(WebTestBase):
    requests_to_load = {
        'IATI Discuss': {
            'url': 'http://discuss.iatistandard.org/?iati-website-tests'
        }
        , 'IATI Discuss Welcome Thread': {
            'url': 'http://discuss.iatistandard.org/t/welcome-to-iati-discuss/6?iati-website-tests'
        }
    }

    def test_contains_links(self, loaded_request):
        """
        Test that each page contains links to the defined URLs.
        """
        result = utility.get_links_from_page(loaded_request)

        assert "http://iatistandard.org/" in result

    @pytest.mark.parametrize("target_request", ["IATI Discuss Welcome Thread"])
    def test_welcome_thread_welcomingness(self, target_request):
        """
        Tests that the Welcome Thread is sufficiently welcoming.
        """
        req = self.loaded_request_from_test_name(target_request)
        title_xpath = '/html/head/title'
        heading_xpath = '//*[@id="main-outlet"]/h1/a'
        subtitle_xpath = '//*[@id="main-outlet"]/div[1]/div[2]/h1'
        post_body_xpath = '//*[@id="main-outlet"]/div[1]/div[2]/p'

        title_text = utility.get_text_from_xpath(req, title_xpath)
        heading_text = utility.get_text_from_xpath(req, heading_xpath)
        subtitle_text = utility.get_text_from_xpath(req, subtitle_xpath)
        post_body_text = utility.get_text_from_xpath(req, post_body_xpath)

        assert utility.substring_in_list('Welcome to IATI Discuss', title_text)
        assert utility.substring_in_list('Welcome to IATI Discuss', heading_text)
        assert utility.substring_in_list('Welcome', subtitle_text)
        assert utility.substring_in_list('Welcome', post_body_text)
