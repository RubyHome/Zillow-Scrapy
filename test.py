import scrapy
import string
# import csv
# from YOUR_PROJECT_NAME_HERE import settings

class obituarySpider(scrapy.Spider):
    name = "obituary"
    # start_urls = [
    #    'http://www.legacy.com/obituaries/wickedlocal-arlington/browse'
    # ]
    API_url = 'http://www.wholefoodsmarket.com/views/ajax'
    scraped_stores = []
    def start_requests(self):
        urls = [
             'http://www.legacy.com/obituaries/wickedlocal-arlington/',
            # 'http://www.legacy.com/obituaries/wickedlocal-malden/',
        ]
        for url in urls:            
            url = url+"browse?page=10"
            print url+"------------------------"
            yield scrapy.Request(url=url, callback=self.parse)    

    def parse(self, response):
        for item in response.xpath('.//div[@class="ListItem__Details___3wfr3"]'):
            
            dataset = {
                 "name" : '',
                 "city" : '',
            }

            name = item.xpath('.//p[@class="ListItem__obitName___2xOrR"]/text()').extract_first()
            dataset["name"] = name
            if "." in name:
                nameArr = name.split(".")
                dataset["name"] = nameArr[1]+" "+nameArr[0]
            city = item.xpath('.//p[@class="ListItem__Location___3P908"]/text()').extract()
            dataset["city"] = city[0]+","+city[2]
            yield dataset
        yield "----------------"


   # def write_to_csv(item):
   #     writer = csv.writer(open(settings.csv_file_path, 'a'), lineterminator='\n')
   #     writer.writerow([item[key] for key in item.keys()])

   # class WriteToCsv(object):
   #      def process_item(self, item, spider):
   #          write_to_csv(item)
   #          return item
