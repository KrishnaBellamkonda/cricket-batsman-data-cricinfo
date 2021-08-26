import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags

ProfileURLS = []

class ProfilelinksSpider(CrawlSpider):
    name = 'ProfileLinks'
    allowed_domains = ['espncricinfo.com']
    start_urls = [
        'https://www.espncricinfo.com/player/adam-gilchrist-5390', 
        'https://www.espncricinfo.com/player/virat-kohli-253802', 
        'https://www.espncricinfo.com/ci/content/player/', 
        'https://www.espncricinfo.com/player/team/australia-2', 
        'https://www.espncricinfo.com/player/team/bangladesh-25', 
        'https://www.espncricinfo.com/player/team/england-1', 
        'https://www.espncricinfo.com/player/team/india-6', 
        'https://www.espncricinfo.com/player/team/new-zealand-5', 
        'https://www.espncricinfo.com/player/team/pakistan-7', 
        'https://www.espncricinfo.com/player/team/south-africa-3', 
        'https://www.espncricinfo.com/player/team/sri-lanka-8',
        'https://www.espncricinfo.com/player/team/west-indies-4', 
        'https://www.espncricinfo.com/player/team/zimbabwe-9'
        ]
    

    # Rules 
    # rule = Rule(LinkExtractor(allow=r'Item'), callback='parse_player', follow=True)
    playerPageLE = Rule(LinkExtractor(allow=r'https:\/\/www\.espncricinfo\.com\/player\/[^\/]*$'), callback='parse_player', follow=True)
    playerPageStatsLE = Rule(LinkExtractor(allow=r'https:\/\/www\.espncricinfo\.com\/player\/.*\/bowling-batting-stats'), callback='parse_item', follow=True)
    playersListPageLE = Rule(LinkExtractor(allow=r'https:\/\/www\.espncricinfo\.com\/player\/team\/.*\/.*$'), follow=True, callback='parse_item')

    rules = (
        playerPageLE, 
        playersListPageLE, 
        playerPageStatsLE
        
    )

    
    def parse_player(self, response):
        url = response.url
        
        # Meta Data 
        nameXPath  = '//p[text() = "Full Name"]/following-sibling::h5/text()'
        bornXPath  = '//p[text() = "Born"]/following-sibling::h5/text()'
        battingStyleXPath  = '//p[text() = "Batting Style"]/following-sibling::h5/text()'
        bowlingStyleXPath  = '//p[text() = "Bowling Style"]/following-sibling::h5/text()'
        playingRoleXPath  = '//p[text() = "Playing Role"]/following-sibling::h5/text()'
        ageXPath  = '//p[text() = "Age"]/following-sibling::h5/text()'
        

        name = response.xpath(nameXPath)
        born = response.xpath(bornXPath)
        battingStyle = response.xpath(battingStyleXPath)
        bowlingStyle = response.xpath(bowlingStyleXPath)
        playingRole = response.xpath(playingRoleXPath)
        age = response.xpath(ageXPath)

        print("NAME:", name)

        # XPaths
        overallTableXPath = "//h5[contains(text(), 'Batting')]/parent::div//table"
        tableHeaderXPath = "./thead/tr/th/text()"
        tableTBodyXPath = "./tbody"
        tRowsXPath = './tr'
        tDXPath = './td/span'

        # Data
        table = response.xpath(overallTableXPath)
        tableHeaders =  table.xpath(tableHeaderXPath)
        headers = [header.extract() for header in tableHeaders] # List of headers 

        tbody = table.xpath(tableTBodyXPath)
        trows = tbody.xpath(tRowsXPath)

        # TData extraction 
        tData = []
        for trow in trows:
            trowData = [remove_tags(td).strip() for td in trow.xpath(tDXPath).extract()]
            tData.append(trowData)
        # tData = [trow.xpath(tDXPath).extract() for trow in trows]

        # Final Dataset 
        player_data = tData.insert(0, headers)
        print("headers;", headers)
        print("player_Data", tData)

        
    
            
        
        # Get data from the 
        
        return {
            "url":url,
           "data": tData, 
           "name":name.extract(), 
           "born":born.extract(), 
           "playingRole":playingRole.extract(), 
           "battingStyle":battingStyle.extract(), 
           "bowlingStyle":bowlingStyle.extract(), 
           "age":age.extract()



           
        }

    def parse_item(self, response):
        url = response.url
        if url not in ProfileURLS:
            ProfileURLS.append(url)

# def parse_player(self, response):
#         url = response.url
        
#         # XPaths
#         overallTableXPath = "//h5[contains(text(), 'Batting')]/parent::div//table"
#         tableHeaderXPath = "./thead/tr/th/text()"

#         # Data
#         table = response.xpath(overallTableXPath)
#         tableHeaders =  table.xpath(tableHeaderXPath)
#         headers = [header.extract() for header in tableHeaders]
#         print(headers)
#         return {
#             "url":url, 

#         }


# def start_requests(self):
#         urls = [
#          "https://www.espncricinfo.com/player/virat-kohli-253802"
#         ]
#         for url in urls:
#             return scrapy.Request(url=url, callback=self.parse_player)