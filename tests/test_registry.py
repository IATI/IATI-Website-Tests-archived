import pytest
from web_test_base import *

class TestIATIRegistry(WebTestBase):
    requests_to_load = {
        'IATI Registry Homepage - http, no www': {
            'url': 'http://iatiregistry.org/'
        }
        , 'IATI Registry Homepage - http, with www': {
            'url': 'http://www.iatiregistry.org/'
        }
        , 'IATI Registry Homepage - https, no www': {
            'url': 'https://iatiregistry.org/'
        }
        , 'IATI Registry Homepage - https, with www': {
            'url': 'https://www.iatiregistry.org/'
        }
        , 'IATI Registry Registration Page': {
            'url': 'https://iatiregistry.org/user/register'
        }
        , 'IATI Registry Login Page': {
            'url': 'https://iatiregistry.org/user/login'
        }
    }

    def test_contains_links(self, loaded_request):
        """
        Test that each page contains links to the defined URLs.
        """
        result = utility.get_links_from_page(loaded_request)

        assert "http://www.aidtransparency.net/" in result
        assert "http://www.iatistandard.org/" in result

    @pytest.mark.parametrize("target_request", ["IATI Registry Registration Page"])
    def test_registration_form_presence(self, target_request):
        """
        Test that there is a valid registration form on the Registry Registration Page.
        """
        req = self.loaded_request_from_test_name(target_request)
        form_xpath = '//*[@id="user-register-form"]'
        form_method_xpath = '//*[@id="user-register-form"]/@method'
        input_xpath = '//*[@id="user-register-form"]/div/div/input'
        button_xpath = '//*[@id="user-register-form"]/div/button'

        forms = utility.locate_xpath_result(req, form_xpath)
        form_method = utility.locate_xpath_result(req, form_method_xpath)
        form_inputs = utility.locate_xpath_result(req, input_xpath)
        form_buttons = utility.locate_xpath_result(req, button_xpath)

        assert len(forms) == 1
        assert form_method == ['post']
        assert len(form_inputs) == 5
        assert len(form_buttons) == 1

    @pytest.mark.parametrize("target_request", ["IATI Registry Login Page"])
    def test_login_form_presence(self, target_request):
        """
        Test that there is a valid login form on the Registry Login Page.
        """
        req = self.loaded_request_from_test_name(target_request)
        form_xpath = '//*[@id="content"]/div[3]/div/section/div/form'
        form_action_xpath = '//*[@id="content"]/div[3]/div/section/div/form/@action'
        form_method_xpath = '//*[@id="content"]/div[3]/div/section/div/form/@method'
        input_xpath = '//*[@id="content"]/div[3]/div/section/div/form/div/div/input'
        button_xpath = '//*[@id="content"]/div[3]/div/section/div/form/div/button'

        forms = utility.locate_xpath_result(req, form_xpath)
        form_action = utility.locate_xpath_result(req, form_action_xpath)
        form_method = utility.locate_xpath_result(req, form_method_xpath)
        form_inputs = utility.locate_xpath_result(req, input_xpath)
        form_buttons = utility.locate_xpath_result(req, button_xpath)

        assert len(forms) == 1
        assert form_action == ['/login_generic?came_from=/user/logged_in']
        assert form_method == ['post']
        assert len(form_inputs) == 2
        assert len(form_buttons) == 1
