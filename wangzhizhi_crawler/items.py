# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlerItem(scrapy.Item):
    crawler_type = scrapy.Field()
    request_url = scrapy.Field()
    response_body = scrapy.Field()

class CityItem(scrapy.Item):
    # define the fields for your item here like:
    city_id = scrapy.Field()
    name = scrapy.Field()
    pass

class StoreItem(scrapy.Item):
    city_id = scrapy.Field()
    store_id = scrapy.Field()
    name = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()
    region = scrapy.Field()
    address = scrapy.Field()
    status = scrapy.Field()
    seat_all = scrapy.Field()
    seat_current_used = scrapy.Field()

class SeatItem(scrapy.Item):
    response_time = scrapy.Field()
    city_id = scrapy.Field()
    store_id = scrapy.Field()
    room_id = scrapy.Field()
    seat_id = scrapy.Field()
    space_id = scrapy.Field()
    space_name = scrapy.Field()
    coordinate_x = scrapy.Field()
    coordinate_y = scrapy.Field()
    user_id = scrapy.Field()
    status = scrapy.Field()

class SeatOccupyItem(scrapy.Item):
    city_id = scrapy.Field()
    store_id = scrapy.Field()
    seat_id = scrapy.Field()
    user_id = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()