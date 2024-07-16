# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


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