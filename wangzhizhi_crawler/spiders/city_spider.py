from wangzhizhi_crawler.spiders.base_spider import BaseSpider
from wangzhizhi_crawler.items import CityItem

import scrapy
import json
import re
from datetime import datetime

class CitySpider(BaseSpider):
    name = "city"

    def start_requests(self):
        req_url = "https://wxa.wangzhizhi.mored.tech/opsli-boot/api/v1/applet/fp/store/org/getStoreArea"
        req_params = {
            "appId": "wxa5cf43f677b9a059"
        }
        yield scrapy.FormRequest(url=req_url, formdata=req_params, method='GET', callback=self.parse)

    def parse(self, response):
        yield self.parse_crawler_item('city', response)

        body = json.loads(response.body)
        for v in body['data']['areaResults']:
            item = CityItem()
            item['city_id'] = int(v['id'])
            item['name'] = v['areaName']
            yield item