import pytest
from web_test_base import *

class TestCSV2IATI(WebTestBase):
    requests_to_load = {
        'CSV2IATI Homepage': {
            'url': 'http://csv2iati.iatistandard.org/'
        }
    }

    def test_contains_links(self, loaded_request):
        """
        Test that each page contains links to the defined URLs.
        """
        result = utility.get_links_from_page(loaded_request)

        assert "http://iatistandard.org" in result

    @pytest.mark.parametrize("target_request", ["CSV2IATI Homepage"])
    def test_login_form_presence(self, target_request):
        """
        Test that there is a valid login form on the CSV2IATI Homepage.
        """
        req = self.loaded_request_from_test_name(target_request)
        form_xpath = '//*[@id="login_register_forms_container"]/fieldset[1]/form'
        form_action_xpath = '//*[@id="login_register_forms_container"]/fieldset[1]/form/@action'
        input_xpath = '//*[@id="login_register_forms_container"]/fieldset[1]/form/dl/dd/input'

        forms = utility.locate_xpath_result(req, form_xpath)
        form_action = utility.locate_xpath_result(req, form_action_xpath)
        form_inputs = utility.locate_xpath_result(req, input_xpath)

        assert len(forms) == 1
        assert form_action == ['/login']
        assert len(form_inputs) == 3

    @pytest.mark.parametrize("target_request", ["CSV2IATI Homepage"])
    def test_registration_form_presence(self, target_request):
        """
        Test that there is a valid registration form on the CSV2IATI Homepage.
        """
        req = self.loaded_request_from_test_name(target_request)
        form_xpath = '//*[@id="login_register_forms_container"]/fieldset[2]/form'
        form_action_xpath = '//*[@id="login_register_forms_container"]/fieldset[2]/form/@action'
        input_xpath = '//*[@id="login_register_forms_container"]/fieldset[2]/form/dl/dd/input'

        forms = utility.locate_xpath_result(req, form_xpath)
        form_action = utility.locate_xpath_result(req, form_action_xpath)
        form_inputs = utility.locate_xpath_result(req, input_xpath)

        assert len(forms) == 1
        assert form_action == ['/register']
        assert len(form_inputs) == 5
