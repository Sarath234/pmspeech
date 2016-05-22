import scrapy


class PMSpeechSpider(scrapy.Spider):
    name = 'pmspeech'
    start_urls = ['http://pmindia.gov.in/en/tag/pmspeech/']

    def parse(self, response):
        for i in range(0, 96):
            yield scrapy.FormRequest(url="http://pmindia.gov.in/wp-admin/admin-ajax.php",
                                     method="POST", formdata={'Referer': 'http://pmindia.gov.in/en/tag/pmspeech/',
                                                              'action': 'infinite_scroll_speeches',
                                                              'page_no': str(i + 1), 'tag': 'pmspeech',
                                                              'loop_file': '10', 'language': 'en',
                                                              'PHPSESSID': 'v35mgdmuse3qqpc1f8qddola8mi839he'},
                                     callback=self.parse_middle)

    def parse_middle(self, response):
        for href in response.css('.news-description h3 a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_speech)

    def parse_speech(self, response):
        yield {
            'date': response.css('.share_date span::text').extract(),
            'title': response.css('.content-block h2::text').extract()[0],
            'speech': response.css('.news-bg p::text').extract(),
            'link': response.url,
        }
