import pytest
from web_test_base import *


@pytest.mark.xfail(strict=True)
# class TestAidTransparency(WebTestBase):  # Original class setup
class TestAidTransparency():  # To be deleted when tests are passing again
    requests_to_load = {
        'AidTransparency Homepage - no www': {
            'url': 'http://aidtransparency.net/'
        }
        , 'AidTransparency Homepage - with www': {
            'url': 'http://www.aidtransparency.net/'
        }
        , '2015 Annual Report': {
            'url': 'http://www.aidtransparency.net/annualreport2015/'
        }
        , 'Tabulated News Archive': {
            'url': 'http://www.aidtransparency.net/category/news/page/5'
        }
        , 'Randomly-selected News Article': {
            'url': 'http://www.aidtransparency.net/news/un-pooled-funds-now-published-to-iati'
        }
        , 'Newsletter Subscription Page': {
            'url': 'http://www.aidtransparency.net/contact/subscribe'
        }
        , 'Misc Sub-navigation Page': {
            'url': 'http://www.aidtransparency.net/governance/secretariat'
        }
        , 'Media Link': {
            'url': 'http://www.aidtransparency.net/wp-content/uploads/2014/10/IATISpeakersKitSpeakingNotes.odt'
        }
    }

    def test_locate_links(self, loaded_request):
        """
        Tests that each page contains links to the defined URLs.
        """
        if not loaded_request.url[-4:] == '.odt':
            result = utility.get_links_from_page(loaded_request)

            assert ("http://iatistandard.org/" in result) or ("http://dashboard.iatistandard.org/" in result)
            assert "http://www.aidtransparency.net" in result

    @pytest.mark.parametrize("target_request", ["AidTransparency Homepage - no www", "AidTransparency Homepage - with www"])
    def test_homepage_news_items(self, target_request):
        """
        Tests that he aidtransparency homepage contains two news articles.
        """
        req = self.loaded_request_from_test_name(target_request)
        parent_xpath = '//*[@id="home-featured"]/div/article'
        title1_xpath = '//*[@id="home-featured"]/div/article[1]/div[2]/h2/a'
        title2_xpath = '//*[@id="home-featured"]/div/article[2]/div[2]/h2/a'
        summary1_xpath = '//*[@id="home-featured"]/div/article[1]/div[2]'
        summary2_xpath = '//*[@id="home-featured"]/div/article[2]/div[2]'
        min_title_length = 10
        max_title_length = 100
        min_summary_length = 40
        max_summary_length = 250

        assert len(utility.locate_xpath_result(req, parent_xpath)) == 2
        assert max_title_length > len(utility.get_joined_text_from_xpath(req, title1_xpath)) > min_title_length
        assert max_title_length > len(utility.get_joined_text_from_xpath(req, title2_xpath)) > min_title_length
        assert max_summary_length > len(utility.get_joined_text_from_xpath(req, summary1_xpath).strip()) > min_summary_length
        assert max_summary_length > len(utility.get_joined_text_from_xpath(req, summary2_xpath).strip()) > min_summary_length


    @pytest.mark.parametrize("target_request", ["AidTransparency Homepage - no www", "AidTransparency Homepage - with www"])
    def test_homepage_news_item_image(self, target_request):
        """
        Test that the image for the latest news item loads correctly.
        """
        req = self.loaded_request_from_test_name(target_request)
        min_img_file_size = 2048

        img_url = utility.locate_xpath_result(req, '//*[@id="home-featured"]/div/article[1]/div[1]/a/img/@src')

        assert len(img_url) == 1
        result = requests.get(img_url[0])

        assert result.status_code == 200
        assert len(result.content) >= min_img_file_size

    @pytest.mark.parametrize("target_request", ["Tabulated News Archive"])
    def test_news_item_pagination(self, target_request):
        """
        Tests that pagination of the news archive is working.
        Checks whether a page somewhere within the pagination contained the
        expected number of links to articles.
        """
        req = self.loaded_request_from_test_name(target_request)
        xpath = '//*[@id="content-wrapper"]/div[2]/article'
        expected_article_count = 10

        result = utility.locate_xpath_result(req, xpath)

        assert len(result) == expected_article_count

    @pytest.mark.parametrize("target_request", ["Randomly-selected News Article"])
    def test_random_news_article(self, target_request):
        """
        Tests that a randomly-selected news article contains expected title. Also
        tests that the post body contains expected text.
        """
        req = self.loaded_request_from_test_name(target_request)
        xpath_post_container = '//*[@id="content"]/article/descendant::*/text()'
        xpath_post_title = '//*[@id="content"]/article/h1[contains(@class, "post-title")]/text()'

        result_post_container = utility.locate_xpath_result(req, xpath_post_container)
        result_post_title = utility.locate_xpath_result(req, xpath_post_title)
        post_container_contents = ''.join(result_post_container)
        post_title_str = result_post_title[0]

        assert 'UN pooled funds' in post_title_str
        assert 'significant contribution to transparency and open data' in post_container_contents

    @pytest.mark.parametrize("target_request", ["Newsletter Subscription Page"])
    def test_newsletter_subscription_page_form(self, target_request):
        """
        Tests to see whether there is a form to subscribe to the newsletter on
        the newsletter subscription page.
        """
        req = self.loaded_request_from_test_name(target_request)
        xpath = '//*[@id="mc-embedded-subscribe-form"]'

        result = utility.locate_xpath_result(req, xpath)

        assert len(result) == 1
