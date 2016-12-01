import pytest
from web_test_base import *

class TestQueryBuilder(WebTestBase):
    requests_to_load = {
        'IATI Query Builder': {
            'url': 'http://datastore.iatistandard.org/query/'
        }
        , 'POST Example': {
            'url': 'http://datastore.iatistandard.org/query/index.php'
            , 'method': 'POST'
            , 'data': {
                'entry.1085079344': 'activity'
                , 'entry.71167035': 'summary'
                , 'entry.1352830161': '50 rows'
                , 'entry.1922375458[]': 'DK-1'
                , 'entry.1954968791[]': '12181'
                , 'entry.1179181326[]': '298'
                , 'submit': 'Submit'
            }
        }
    }

    def test_locate_links(self, loaded_request):
        """
        Tests that a page contains links to the defined URLs.
        """
        result = utility.get_links_from_page(loaded_request)

        assert "http://datastore.iatistandard.org/" in result

    @pytest.mark.parametrize("target_request", ["POST Example"])
    def test_form_submit_link(self, target_request):
        """
        Tests that a result page contains a link to the relevant search.
        """
        req = self.loaded_request_from_test_name(target_request)

        result = utility.get_links_from_page(req)

        assert "http://datastore.iatistandard.org/api/1/access/activity.csv?reporting-org=DK-1&sector=12181&recipient-region=298" in result
