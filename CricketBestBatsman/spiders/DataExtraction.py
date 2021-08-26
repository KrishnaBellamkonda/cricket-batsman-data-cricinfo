import scrapy
from w3lib.html import remove_tags

class DataextractionSpider(scrapy.Spider):
    name = 'DataExtraction'
    allowed_domains = ['espncricinfo.com']
    start_urls = ["https://www.espncricinfo.com/player/sachin-tendulkar-35320"]

    def parse(self, response):
        url = response.url
        
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

        # Data extraction 
        tData = []
        for trow in trows:
            trowData = [remove_tags(td).strip() for td in trow.xpath(tDXPath).extract()]
            tData.append(trowData)

        # tData = [[td] for trow in trows for td in  trow.xpath(tDXPath).extract()]
        print(tData)

        # Final Dataset 
        player_data = tData.insert(0, headers)
        # print("headers;", headers)
        print("player_Data", tData)


        
        return {
            "url":url,
           "data": tData
        }
