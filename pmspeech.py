import scrapy


class PMSpeechSpider(scrapy.Spider):
    name = 'pmspeech'
    start_urls = ['http://archivepmo.nic.in/abv/all-speeches.php',
                  'http://archivepmo.nic.in/drmanmohansingh/all-speeches.php']
    # start_urls = ['http://archivepmo.nic.in/drmanmohansingh/all-speeches.php']

    def parse(self, response):
        for href in response.css('.speechPan ul a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_speech)

    def parse_speech(self, response):
        yield {
            'datenplace': response.xpath('//h2[@class="date"]/text()').extract(),
            'title': response.css('.innerHead::text').extract()[0],
            'speech1': response.css('.rt p span::text').extract(),
            'speech2': response.css('.rt p font::text').extract(),
            'speech3': response.css('.rt p::text').extract(),
            'link': response.url,
        }
