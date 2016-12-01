import pytest
from web_test_base import *

class TestIATIPreview(WebTestBase):
    requests_to_load = {
        'IATI Preview': {
            'url': 'http://preview.iatistandard.org/'
        }
        , 'Valid (Example) XML Input': {
            'url': 'http://preview.iatistandard.org/index.php?url=https%3A%2F%2Fraw.githubusercontent.com%2FIATI%2FIATI-Extra-Documentation%2Fversion-2.01%2Fen%2Factivity-standard%2Factivity-standard-example-annotated.xml'
        }
        , 'Non-XML Input': {
            'url': 'http://preview.iatistandard.org/index.php?url=http%3A%2F%2Fpreview.iatistandard.org%2Findex.php'
        }
    }

    def test_contains_links(self, loaded_request):
        """
        Test that each page contains links to the defined URLs.
        """
        result = utility.get_links_from_page(loaded_request)

        assert "http://www.iatistandard.org/" in result

    @pytest.mark.parametrize("target_request", ["IATI Preview"])
    def test_web_address_form_presence(self, target_request):
        """
        Test that there is a form to enter a URL of a valid XML file on the Preview Tool.
        """
        req = self.loaded_request_from_test_name(target_request)
        form_xpath = '//*[@id="main"]/div/div/div[1]/div/form'
        form_action_xpath = '//*[@id="main"]/div/div/div[1]/div/form/@action'
        form_method_xpath = '//*[@id="main"]/div/div/div[1]/div/form/@method'
        input_xpath = '//*[@id="url"]'
        button_xpath = '//*[@id="main"]/div/div/div[1]/div/form/div/div/span/button'

        forms = utility.locate_xpath_result(req, form_xpath)
        form_action = utility.locate_xpath_result(req, form_action_xpath)
        form_method = utility.locate_xpath_result(req, form_method_xpath)
        form_inputs = utility.locate_xpath_result(req, input_xpath)
        form_buttons = utility.locate_xpath_result(req, button_xpath)

        assert len(forms) == 1
        assert form_action == ['index.php']
        assert form_method == ['get']
        assert len(form_inputs) == 1
        assert len(form_buttons) == 1

    @pytest.mark.parametrize("target_request", ["Valid (Example) XML Input"])
    def test_example_xml_detection(self, target_request):
        """
        Test that valid XML is detected and parsed.
        """
        req = self.loaded_request_from_test_name(target_request)
        activity_count_xpath = '//*[@id="main"]/div/div/div[1]/div'
        policy_marker_2_xpath = '//*[@id="actinfo-AA-AAA-123456789-ABC123-0"]/li[26]/div/span[2]'

        activity_count_text = utility.get_text_from_xpath(req, activity_count_xpath)
        policy_marker_2_text = utility.get_text_from_xpath(req, policy_marker_2_xpath)

        assert utility.substring_in_list('This file has 1 activity', activity_count_text)
        assert utility.substring_in_list(' [vocabulary="1"\xa0code="1"\xa0significance="4"\xa0]', policy_marker_2_text)

    @pytest.mark.parametrize("target_request", ["Non-XML Input"])
    def test_non_xml_detection(self, target_request):
        """
        Test that a URL that is not XML is detected as such.
        """
        req = self.loaded_request_from_test_name(target_request)
        failed_detection_xpath = '//*[@id="main"]/div/div/div[1]'

        failed_detection_text = utility.get_text_from_xpath(req, failed_detection_xpath)

        assert utility.substring_in_list('Sorry, could not get IATI compliant data from the supplied file!', failed_detection_text)
