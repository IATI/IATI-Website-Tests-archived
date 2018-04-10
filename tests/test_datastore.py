from datetime import date, datetime, timedelta
import pytest
import requests
from web_test_base import *


class TestIATIDatastore(WebTestBase):
    requests_to_load = {
        'Datastore Homepage': {
            'url': 'http://datastore.iatistandard.org/'
        },
        'API - Activities Updated since 2 days ago': {
            'url': 'http://datastore.iatistandard.org/api/1/access/activity.xml?limit=0&last-updated-datetime__gt=' + str(date.today() - timedelta(days=2)),
            'min_response_size': 295
        },
        'API - Activities Updated since 3 days ago': {
            'url': 'http://datastore.iatistandard.org/api/1/access/activity.xml?limit=0&last-updated-datetime__gt=' + str(date.today() - timedelta(days=3)),
            'min_response_size': 295
        },
        'Datastore download: csv': {
            'url': 'http://datastore.iatistandard.org/api/1/access/activity.csv'
        },
        'Datastore download: xml': {
            'url': 'http://datastore.iatistandard.org/api/1/access/activity.xml'
        },
        'Datastore download: json': {
            'url': 'http://datastore.iatistandard.org/api/1/access/activity.json'
        },
        'Datastore list of datasets': {
            'url': 'http://datastore.iatistandard.org/api/1/about/datasets/fetch_status'
        }
    }

    @pytest.mark.xfail
    @pytest.mark.parametrize("target_request", ["Datastore Homepage"])
    def test_contains_links(self, target_request):
        """Test that each page contains links to the defined URLs."""
        loaded_request = self.loaded_request_from_test_name(target_request)

        result = utility.get_links_from_page(loaded_request)

        assert "http://iatiregistry.org/" in result

    @pytest.mark.parametrize("target_request", ["API - Activities Updated since 2 days ago", "API - Activities Updated since 3 days ago"])
    def test_recent_activities(self, target_request):
        """Test that the datastore API knows of activities updated in the past few days."""
        req = self.loaded_request_from_test_name(target_request)
        xpath = '//result/iati-activities/query/total-count'

        result = utility.get_single_int_from_xpath(req, xpath)

        assert result > 0

    @pytest.mark.parametrize("content_type", ["application/xml", "application/json", "text/csv"])
    def test_api_output_filetype(self, content_type):
        """
        Test that API calls return data in the expected filetypes.

        The test is conducted based upon the data returned in the request
        headers["content-type"]. For example, 'application/xml; charset=utf-8'
        """
        file_extenstion = content_type.split("/")[1]
        loaded_request = self.loaded_request_from_test_name("Datastore download: {}".format(file_extenstion))

        result = loaded_request.headers["content-type"]

        assert result.startswith(content_type)

    @pytest.mark.parametrize("target_request", ["Datastore list of datasets"])
    def test_last_successful_fetch(self, target_request):
        """Test that the datastore has successfully fetched data within the expected time frame."""
        loaded_request = self.loaded_request_from_test_name(target_request)
        successful_fetch_dates = list()
        json_datasets = loaded_request.json()
        list_of_datasets = json_datasets['datasets']

        resources = [list(dataset.values())[0] for dataset in list_of_datasets]
        successful_fetch_dates = [datetime.strptime(resource['last_successful_fetch'][:10], '%Y-%m-%d') for resource in resources if resource['last_successful_fetch'] is not None]

        assert max(successful_fetch_dates) >= (datetime.now() - timedelta(days=7))
