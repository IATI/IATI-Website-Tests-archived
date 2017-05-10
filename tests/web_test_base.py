import pytest
import requests

from utility import utility

class WebTestBase:
    """This is a base class for all web tests.

    Attributes:
        requests_to_load (dict):    A dictionary of web requests required for tests.
            Values within the dictionary are themselves dictionaries holding
            further information about the request.
            {
                'test_name': {
                    'url (str)': The URL to load for this test
                    , 'min_response_size (int, optional)': An integer value
                        specifying the minimum size in bytes that the response
                        should be.
                        If not be set, a default value is utilised.
                    , 'method (str, optional)': A string stating the HTTP method
                        to be used by the request. Defaults to `GET`.
                        Additionally supports `POST`.
                    , 'data (optional)': {
                        'key': 'value'
                        , 'key2': 'value2'
                        , ...
                            A dictionary containing any data to send with a POST
                            request.
                    }
                }
            }
        loaded_requests (dict):     A dictionary of web requests that have been loaded.
            The keys to this dictionary are the `test_name` keys from
            `requests_to_load`.
            The values are `Request` objects from the `requests` library.
        initial_num_urls_to_test (int): The number of URLs specified within this
            base class. Must not be overwritten by child classes.
            Used within a test to ensure the class is being inherited from
            correctly, with child classes defining their own requests_to_load.
    """

    requests_to_load = dict()
    initial_num_urls_to_test = len(requests_to_load)
    loaded_requests = dict()

    def loaded_request_from_test_name(self, test_name):
        """
        Returns the loaded request for a given URL.
        """
        return self.loaded_requests[test_name]

    def passes_text_detection_test(self, target_request, text_to_find, xpath_to_locate):
        """
        Performs a test to see whether the specified text is located within
        the request with a given name at the given xpath.
        Returns True if the text exists correctly, else False.
        """
        req = self.loaded_request_from_test_name(target_request)

        result = utility.get_text_from_xpath(req, xpath_to_locate)

        return utility.substring_in_list(text_to_find, result)

    @classmethod
    def setup_class(cls):
        """
        Initialise the class
        Loads data from each of the required URLs
        """
        for testname, test in cls.requests_to_load.items():
            try:
                method = test['method']
            except KeyError:
                method = 'GET'

            if method == 'GET':
                result = requests.get(test['url'])
            elif method == 'POST':
                result = requests.post(test['url'], data=test['data'])
            else:
                raise ValueError('Invalid HTTP method - ' + method)

            cls.loaded_requests[testname] = result
        cls.num_urls = len(cls.requests_to_load)

    def pytest_generate_tests(cls, metafunc):
        """
        Dynamically parametrizes fixtures after initialisation
        """
        if 'request_to_load' in metafunc.fixturenames:
            metafunc.parametrize("request_to_load", cls.requests_to_load.keys())
        if 'text_to_find' in metafunc.fixturenames:
            metafunc.parametrize("text_to_find", cls.text_to_find)

    @pytest.fixture
    def loaded_request(cls, request_to_load):
        """
        Converts the parametrized URL into loaded Request object that has
        already been initialised.
        """
        return cls.loaded_requests[request_to_load]

    def test_200_response(self, loaded_request):
        """
        Tests that each loaded request has a status code of 200.
        """
        assert loaded_request.status_code == 200

    def test_non_tiny_response(self, request_to_load):
        """
        Tests that each loaded request has response content that is not tiny.
        """
        try:
            min_response_size = self.requests_to_load[request_to_load]['min_response_size']
        except KeyError:
            min_response_size = 4000
        req = self.loaded_request_from_test_name(request_to_load)

        if req.encoding:
            result = req.content.decode(req.encoding)
        else:
            result = req.content.decode()

        assert len(result) >= min_response_size

    def test_num_urls(self):
        """
        Ensure that urls from a child class are being correctly detected
        """
        assert len(self.requests_to_load) > self.initial_num_urls_to_test
