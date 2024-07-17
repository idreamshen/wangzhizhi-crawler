from wangzhizhi_crawler.spiders.base_spider import BaseSpider
from wangzhizhi_crawler.items import StoreItem

import scrapy
import json
import re
from datetime import datetime

class StoreSpider(BaseSpider):
    name = "store"

    def start_requests(self):
        cities = self.find_all_city()
        for v in cities:
            req_url = "https://wxa.wangzhizhi.mored.tech/opsli-boot/api/v1/applet/fp/store/org/getStoreBrief"
            req_params = {
                "pageNo": "1",
                "pageSize": "500",
                "cityId": str(v.city_id),
                "appId": "wxa5cf43f677b9a059"
            }

            yield scrapy.FormRequest(url=req_url, formdata=req_params, method="GET", callback=self.parse, meta={
                'city_id': v.city_id,
            })

    def parse(self, response):
        yield self.parse_crawler_item('store', response)

        body = json.loads(response.body)
        for v in body['data']['storeBriefList']:
            item = StoreItem()
            item['city_id'] = response.meta['city_id']
            item['store_id'] = int(v['id'])
            item['name'] = v['storeName']
            item['lon'] = float(v['storeLon'])
            item['lat'] = float(v['storeLat'])
            item['region'] = v['storeAreaName']
            item['address'] = v['storeAreaTotal']
            item['status'] = v['storeStatus']
            item['seat_all'] = v['storeSeatAll']
            item['seat_current_used'] = v['storeSeatUsed']

            yield item