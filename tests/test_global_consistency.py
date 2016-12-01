import pytest
from web_test_base import *

class TestGlobalConsistency(WebTestBase):
    requests_to_load = {
        'IATI Registry - Homepage': {
            'url': 'https://iatiregistry.org/'
        }
        , 'IATI Registry - Activity Dataset Page': {
            'url': 'https://iatiregistry.org/dataset?q=&filetype=Activity'
        }
        , 'IATI Registry - Organisation Dataset Page': {
            'url': 'https://iatiregistry.org/dataset?q=&filetype=Organisation'
        }
        , 'IATI Registry - organization Dataset Page': {
            'url': 'https://iatiregistry.org/dataset?q=&filetype=organization'
        }
        , 'IATI Dashboard - Homepage': {
            'url': 'http://dashboard.iatistandard.org/'
        }
        , 'IATI Dashboard - Activities Page': {
            'url': 'http://dashboard.iatistandard.org/activities.html'
        }
        , 'IATI Dashboard - Files Page': {
            'url': 'http://dashboard.iatistandard.org/files.html'
        }
        , 'IATI Dashboard - Publisher Page': {
            'url': 'http://dashboard.iatistandard.org/publishers.html'
        }
        , 'Datastore API - Activity Count': {
            'url': 'http://datastore.iatistandard.org/api/1/access/activity.xml?limit=0'
            , 'min_response_size': 295
        }
    }

    def _locate_int_on_page(self, test_name, xpath):
        req = self.loaded_request_from_test_name(test_name)
        result = utility.get_single_int_from_xpath(req, xpath)
        return result

    @pytest.fixture
    def dash_home_activity_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Homepage', '//*[@id="wrap"]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[1]/a')

    @pytest.fixture
    def dash_home_unique_activity_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Homepage', '//*[@id="wrap"]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[2]/td[1]/a')

    @pytest.fixture
    def dash_home_activity_file_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Homepage', '//*[@id="wrap"]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[4]/td[1]/a')

    @pytest.fixture
    def dash_home_org_file_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Homepage', '//*[@id="wrap"]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[1]/a')

    @pytest.fixture
    def dash_home_publisher_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Homepage', '//*[@id="wrap"]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[3]/td[1]/a')

    @pytest.fixture
    def dash_activities_activity_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Activities Page', '//*[@id="wrap"]/div[2]/div[2]/div[1]/div/div[1]/h3/span[1]')

    @pytest.fixture
    def dash_activities_unique_activity_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Activities Page', '//*[@id="wrap"]/div[2]/div[2]/div[2]/div/div[1]/h3/span[1]')

    @pytest.fixture
    def dash_files_activity_file_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Files Page', '//*[@id="wrap"]/div[2]/div[2]/div[1]/div/div[1]/h3/span[1]')

    @pytest.fixture
    def dash_files_org_file_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Files Page', '//*[@id="wrap"]/div[2]/div[2]/div[2]/div/div[1]/h3/span[1]')

    @pytest.fixture
    def dash_publishers_publisher_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Publisher Page', '//*[@id="wrap"]/div[2]/div[2]/div[1]/div/div[1]/h3/span[1]')

    @pytest.fixture
    def datastore_api_activity_count(cls):
        return cls._locate_int_on_page('Datastore API - Activity Count', '//result/iati-activities/query/total-count')

    @pytest.fixture
    def registry_home_publisher_count(cls):
        return cls._locate_int_on_page('IATI Registry - Homepage', '//*[@id="home-icons"]/div/div[2]/div/a/strong')

    @pytest.fixture
    def registry_activity_file_count(cls):
        return cls._locate_int_on_page('IATI Registry - Activity Dataset Page', '//*[@id="content"]/div[3]/div/section[1]/div[1]/form/h2')

    @pytest.fixture
    def registry_organisation_file_count(cls):
        return cls._locate_int_on_page('IATI Registry - Organisation Dataset Page', '//*[@id="content"]/div[3]/div/section[1]/div[1]/form/h2')

    @pytest.fixture
    def registry_organization_file_count(cls):
        return cls._locate_int_on_page('IATI Registry - organization Dataset Page', '//*[@id="content"]/div[3]/div/section[1]/div[1]/form/h2')

    @pytest.fixture
    def registry_all_org_file_count(cls, registry_organisation_file_count, registry_organization_file_count):
        return registry_organisation_file_count + registry_organization_file_count

    def test_activity_count_above_min(self, dash_home_activity_count, dash_home_unique_activity_count, dash_activities_activity_count, dash_activities_unique_activity_count, datastore_api_activity_count):
        """
        Test to ensure the unique activity count is above a specified minumum value.
        This checks both the dashboard and datastore.
        """
        min_activity_count = 550000

        assert dash_home_activity_count >= min_activity_count
        assert dash_home_unique_activity_count >= min_activity_count
        assert dash_activities_activity_count >= min_activity_count
        assert dash_activities_unique_activity_count >= min_activity_count
        assert datastore_api_activity_count >= min_activity_count

    def test_activity_count_dash_value_consistency(self, dash_home_activity_count, dash_home_unique_activity_count, dash_activities_activity_count, dash_activities_unique_activity_count):
        """
        Test to ensure activity counts are consistent within the dashboard.
        """
        assert dash_home_activity_count == dash_activities_activity_count
        assert dash_home_unique_activity_count == dash_activities_unique_activity_count

    def test_unique_vs_total_dash_activity_values(self, dash_home_activity_count, dash_home_unique_activity_count, dash_activities_activity_count, dash_activities_unique_activity_count):
        """
        Test to ensure unique activity counts within the dashboard are not higher
        than the overall activity counts.
        """
        assert dash_home_activity_count >= dash_home_unique_activity_count
        assert dash_activities_activity_count >= dash_activities_unique_activity_count

    def test_activity_count_consistency(self, datastore_api_activity_count, dash_home_unique_activity_count):
        """
        Test to ensure the activity count is consistent, within a margin of error,
        between the datastore and dashboard.
        """
        max_datastore_disparity = 0.1

        assert datastore_api_activity_count >= dash_home_unique_activity_count * (1 - max_datastore_disparity)
        assert datastore_api_activity_count <= dash_home_unique_activity_count * (1 + max_datastore_disparity)

    def test_activity_file_count_above_min(self, registry_activity_file_count, dash_home_activity_file_count, dash_files_activity_file_count):
        """
        Test to ensure the unique activity file count is above a specified minumum value.
        This checks both the dashboard and registry.
        """
        min_file_count = 4100

        assert registry_activity_file_count >= min_file_count
        assert dash_home_activity_file_count >= min_file_count
        assert dash_files_activity_file_count >= min_file_count

    def test_activity_file_count_dash_values(self, dash_home_activity_file_count, dash_files_activity_file_count):
        """
        Test to ensure activity file counts are consistent within the dashboard.
        """
        assert dash_home_activity_file_count == dash_files_activity_file_count

    def test_activity_file_count_consistency(self, registry_activity_file_count, dash_home_activity_file_count, dash_files_activity_file_count):
        """
        Test to ensure the activity file count is consistent, within a margin of error,
        between the registry and dashboard.
        """
        max_registry_disparity = 0.025

        assert registry_activity_file_count >= dash_files_activity_file_count * (1 - max_registry_disparity)
        assert registry_activity_file_count <= dash_files_activity_file_count * (1 + max_registry_disparity)

    def test_org_file_count_above_min(self, registry_all_org_file_count, dash_home_org_file_count, dash_files_org_file_count):
        """
        Test to ensure the organisation file count is above a specified minumum value.
        This checks both the dashboard and registry.
        """
        min_file_count = 350

        assert registry_all_org_file_count >= min_file_count
        assert dash_home_org_file_count >= min_file_count
        assert dash_files_org_file_count >= min_file_count

    def test_org_file_count_dash_values(self, dash_home_org_file_count, dash_files_org_file_count):
        """
        Test to ensure organisation file counts are consistent within the dashboard.
        """
        assert dash_home_org_file_count == dash_files_org_file_count

    def test_organisation_dataset_count_consistency(self, registry_all_org_file_count, dash_home_org_file_count, dash_files_org_file_count):
        """
        Test to ensure the activity file count is consistent, within a margin of error,
        between the registry and dashboard.
        """
        max_registry_disparity = 0.05

        assert registry_all_org_file_count >= dash_files_org_file_count * (1 - max_registry_disparity)
        assert registry_all_org_file_count <= dash_files_org_file_count * (1 + max_registry_disparity)

    def test_publisher_count_above_min(self, registry_home_publisher_count, dash_home_publisher_count, dash_publishers_publisher_count):
        """
        Test to ensure the publisher count is above a specified minumum value.
        This checks both the dashboard and registry.
        """
        min_publisher_count = 480

        assert registry_home_publisher_count >= min_publisher_count
        assert dash_home_publisher_count >= min_publisher_count
        assert dash_publishers_publisher_count >= min_publisher_count

    def test_publisher_count_dash_values(self, dash_home_publisher_count, dash_publishers_publisher_count):
        """
        Test to ensure organisation file counts are consistent within the dashboard.
        """
        assert dash_home_publisher_count == dash_publishers_publisher_count

    def test_publisher_count_consistency(self, registry_home_publisher_count, dash_home_publisher_count):
        """
        Test to ensure the activity file count is consistent, within a margin of error,
        between the registry and dashboard.
        """
        max_registry_disparity = 0.01

        assert registry_home_publisher_count >= dash_home_publisher_count * (1 - max_registry_disparity)
        assert registry_home_publisher_count <= dash_home_publisher_count * (1 + max_registry_disparity)
