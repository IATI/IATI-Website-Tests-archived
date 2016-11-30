from datetime import date, timedelta
import pytest
from web_test_base import *

class TestIATIDatastore(WebTestBase):
    requests_to_load = {
        'Datastore Homepage': {
            'url': 'http://datastore.iatistandard.org/'
        }
        , 'API - Activities Updated Since Yesterday': {
            'url': 'http://datastore.iatistandard.org/api/1/access/activity.xml?limit=0&last-updated-datetime__gt=' + str(date.today() - timedelta(days=1))
            , 'min_response_size': 295
        }
    }

    @pytest.mark.parametrize("target_request", ["Datastore Homepage"])
    def test_contains_links(self, target_request):
        """
        Test that each page contains links to the defined URLs.
        """
        loaded_request = self.loaded_request_from_test_name(target_request)

        result = utility.get_links_from_page(loaded_request)

        assert "http://iatiregistry.org/" in result

    @pytest.mark.parametrize("target_request", ["API - Activities Updated Since Yesterday"])
    def test_recent_activities(self, target_request):
        """
        Test that the datastore API knows of activities updated in the past
        couple of days.
        """
        req = self.loaded_request_from_test_name(target_request)
        xpath = '//result/iati-activities/query/total-count'

        result = utility.get_single_int_from_xpath(req, xpath)

        assert result > 0
