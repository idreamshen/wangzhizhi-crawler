import scrapy
from wangzhizhi_crawler.items import CrawlerItem
from wangzhizhi_crawler.db import DBSession
from wangzhizhi_crawler.entity.city import City
from wangzhizhi_crawler.entity.store import Store
from wangzhizhi_crawler.entity.seat import Seat

class BaseSpider(scrapy.Spider):

    def parse_crawler_item(self, crawler_type, response):
        item = CrawlerItem()
        item['crawler_type'] = crawler_type
        item['request_url'] = response.url
        item['response_body'] = response.body
        return item
    
    def find_all_city(self):
        with DBSession() as session:
            return session.query(City).all()

    def find_all_store(self):
        with DBSession() as session:
            return session.query(Store).all()

    def find_all_seat(self):
        with DBSession() as session:
            return session.query(Seat).all()