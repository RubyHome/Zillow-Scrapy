import scrapy
import string
import pdb

class demoSpider(scrapy.Spider):
    name = "demo"
    url_template = "http://www.zillow.com/homes/for_sale/%s/fsba,fsbo_lt/%s_duplex_type/31471_rid/%d-_beds/%s_price/19-96_mp/globalrelevanceex_sort/38.389571,-86.888123,37.640878,-88.312226_rect/9_zm/0_mmm/"
         
    num = 0           
    def __init__(self):
        self.city_name = "Evansville IN"
        self.price = [5000, 25000]
        self.beds = 1
        self.home_type = ["house", "apartment"]
    def __init__(self, cityName='', domain=None, *args, **kwargs):
        self.city_name = 0
        self.price = 
        self.beds =
        self.home_type = 

    def start_requests(self):
        url = self.url_template % (self.city_name.replace(" ", "-"), ",".join(self.home_type), self.beds, "-".join([str(item) for item in self.price]))
        
        print url
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pagenation = response.xpath('//div[@class="zsg-content-item"]//ol//li//a/@href').extract_first()
        for photo in response.xpath('//ul[@class="photo-cards"]//li'):
            next_page = photo.xpath('article//div[@class="zsg-photo-card-content zsg-aspect-ratio-content"]//a/@href').extract_first()
            #pdb.set_trace()
            if next_page is not None:
                next_page = "http://www.zillow.com"+next_page
                yield scrapy.Request(next_page, callback=self.detail_page)

        if pagenation is not None:
            pagenation= response.urljoin(pagenation)
            yield scrapy.Request(pagenation,callback=self.parse)

    def detail_page(self, response):
            self.num += 1
        #pdb.set_trace();

            item = {
                'MLS' : '',
                'Single Family' : '',
                'Price/sqft' : '',
                'Built in' : '',
                'state' : self.remove_special_char(response.xpath('//div[@class="zsg-layout-breadcrumbs"]//ol//li[1]//a/text()').extract_first()),
                'city' : self.remove_special_char(response.xpath('//div[@class="zsg-layout-breadcrumbs"]//ol//li[2]//a/text()').extract_first()),
                'zip_code' : self.remove_special_char(response.xpath('//div[@class="hdp-content-wrapper zsg-content-section"]//div[@class="zsg-lg-2-3 zsg-sm-1-1 hdp-header-description"]//h1[@class="notranslate"]//span/text()').extract_first().split(",")[-1].strip()),
                'Lot' : '',
                'price' : self.remove_special_char(response.xpath('//div[@class="zsg-lg-1-3 zsg-md-1-1 hdp-summary"]//div[@class="estimates"]//div[@class="main-row  home-summary-row"]//span/text()').extract_first()),
                'zestimate' :  self.remove_special_char(response.xpath('//div[@class="zest-value"]/text()').extract_first()),
                'zestimate_rent' :  self.remove_special_char(response.xpath('//div[@class="zest-value"]')[1].xpath("./text()").extract_first()),
                'bedrooms' : self.remove_special_char(response.xpath('//div[@class="hdp-content-wrapper zsg-content-section"]//div[@class="zsg-lg-2-3 zsg-sm-1-1 hdp-header-description"]//h3//span[@class="addr_bbs"][1]/text()').extract_first()),
                'baths' : self.remove_special_char(response.xpath('//div[@class="hdp-content-wrapper zsg-content-section"]//div[@class="zsg-lg-2-3 zsg-sm-1-1 hdp-header-description"]//h3//span[@class="addr_bbs"][2]/text()').extract_first()),
                'address' : self.remove_special_char(response.xpath('//div[@class="hdp-content-wrapper zsg-content-section"]//div[@class="zsg-lg-2-3 zsg-sm-1-1 hdp-header-description"]//h1[@class="notranslate"]/text()').extract_first() + 
                          response.xpath('//div[@class="hdp-content-wrapper zsg-content-section"]//div[@class="zsg-lg-2-3 zsg-sm-1-1 hdp-header-description"]//h1[@class="notranslate"]//span/text()').extract_first()) ,
                'url' : response.url,
                'description' : self.remove_special_char(response.xpath('//section//div[@class="notranslate zsg-content-item"]/text()').extract_first()),
            }
            
            attributes = []
            nodes = response.xpath("//div[@class='fact-group-container zsg-content-component top-facts']")[0].xpath(".//li/text()")
            for node in nodes:
                attributes.append(node.extract())
 
            for scrapy_attr in ["Built in","Price/sqft","MLS","Single Family","Lot"]:
                result = [attr for attr in attributes if scrapy_attr in attr]
               
                if len(result) > 0:
                    item[scrapy_attr] = self.remove_special_char(result[0])     

            yield item

    def remove_special_char(self, str_var):
        if str_var:
            str_var = str_var.replace(";","")
            return str_var.replace(",", "")
        return None
