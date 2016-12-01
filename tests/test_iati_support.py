import pytest
from web_test_base import *

class TestIATISupport(WebTestBase):
    requests_to_load = {
        'IATI Support Landing Page': {
            'url': 'http://support.iatistandard.org/hc/en-us'
        }
    }
