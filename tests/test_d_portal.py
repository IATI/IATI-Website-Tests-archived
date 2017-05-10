import pytest
from web_test_base import *

class TestDPortal(WebTestBase):
    requests_to_load = {
        'D-Portal Homepage': {
            'url': 'http://d-portal.org/'
            , 'min_response_size': 1100
        }
    }

    @pytest.mark.xfail(strict=True)
    def test_200_response(self, loaded_request):
        super(TestDPortal, self).test_200_response(loaded_request)

    @pytest.mark.xfail(strict=True)
    def test_non_tiny_response(self, loaded_request):
        super(TestDPortal, self).test_non_tiny_response(loaded_request)
