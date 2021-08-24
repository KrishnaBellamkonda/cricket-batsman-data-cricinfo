import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrickbuzzprofilesSpider(CrawlSpider):
    name = 'CrickBuzzProfiles'
    allowed_domains = ['cricbuzz.com']
    start_urls = [
        'https://www.cricbuzz.com/cricket-stats/icc-rankings/men/batting',

    ]

    # Rules 
    playerPageLE = Rule(LinkExtractor(allow=r'https:\/\/www\.cricbuzz\.com\/profiles\/.*'), callback='parse_item', follow=True)
    matchPageLE = Rule(LinkExtractor(allow=r'https:\/\/www\.cricbuzz\.com\/live-cricket-scorecard\/.*\/*.'), callback='parse_item', follow=True)

    rules = (
        playerPageLE,
        matchPageLE

    )

    def parse_item(self, response):
        item = {
            "url":response.url
        }
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
