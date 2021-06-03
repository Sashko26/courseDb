import scrapy
global page

from twisted.internet import defer
from scrapy.crawler import CrawlerRunner
from dbSettings import db

def _run_crawler(spider_cls):
    runner = CrawlerRunner()
    return runner.crawl(spider_cls)     # return Deferred

def _success(results):    return results
def _error(failure):
    print("it is baad")
    return failure

def test_multiple_crawls(Spider):
    d1 = _run_crawler(Spider)
    d_list = defer.gatherResults([d1])
    return d_list

class BLogSpider(scrapy.Spider):
    name = 'blogspider'
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def __init__(self, *args, **kwargs):
        super(BLogSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        self.search_request =kwargs.get('search_request')
        self.time_of_request=kwargs.get('time_of_request')
        self.page = 0



    def parse(self, response):

        for smartphone in response.css('tr.wrap'):
            titleWrraper = smartphone.css('h3.lheight22.margintop5')
            titleStrong = titleWrraper.css('a strong::text').getall()[0]
            divPrice = smartphone.css('.space.inlblk.rel')
            price = divPrice.css('p strong::text').getall()[0]
            link = titleWrraper.css('a.marginright5.link.linkWithHash.detailsLink::attr(href)').getall()[0]



            if titleStrong.upper().find(self.search_request.upper()) !=-1:
                print(titleStrong)
                db.insert(titleStrong,price,link,self.time_of_request)

        self.page = self.page + 1
        print(self.page)
        if self.page<=25:
            yield response.follow(url=self.start_urls[0]+"?page="+str(self.page), callback=self.parse)











