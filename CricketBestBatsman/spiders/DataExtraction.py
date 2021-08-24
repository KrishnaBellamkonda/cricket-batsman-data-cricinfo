import scrapy


class DataextractionSpider(scrapy.Spider):
    name = 'DataExtraction'
    allowed_domains = ['espncricinfo.com']
    start_urls = ["https://www.espncricinfo.com/player/virat-kohli-253802"]

    def parse(self, response):
        url = response.url
        
        # XPaths
        overallTableXPath = "//h5[contains(text(), 'Batting')]/parent::div//table"
        tableHeaderXPath = "./thead/tr/th/text()"
        tableTBodyXPath = "./tbody"
        tRowsXPath = './tr'
        tDXPath = './td/span/text()'

        # Data
        table = response.xpath(overallTableXPath)
        tableHeaders =  table.xpath(tableHeaderXPath)
        headers = [header.extract() for header in tableHeaders] # List of headers 

        tbody = table.xpath(tableTBodyXPath)
        trows = tbody.xpath(tRowsXPath)
        tData = [trow.xpath(tDXPath).extract() for trow in trows]

        # Final Dataset 
        player_data = tData.insert(0, headers)
        print("headers;", headers)
        print("player_Data", tData)


        
        return {
            "url":url,
           "data": tData
        }
