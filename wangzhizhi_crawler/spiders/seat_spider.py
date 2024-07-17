from wangzhizhi_crawler.spiders.base_spider import BaseSpider
from wangzhizhi_crawler.items import SeatItem, SeatOccupyItem

import scrapy
import json
import re
from datetime import datetime

class SeatSpider(BaseSpider):
    name = "seat"

    def start_requests(self):
        stores = self.find_all_store()
        for v in stores:
            req_url = f"https://wxa.wangzhizhi.mored.tech/opsli-boot/api/v1/applet/store/live_situation/query"
            today_str = datetime.now().strftime("%Y-%m-%d")
            req_params = {
                "storeId": str(v.store_id),
                "startTime": f"{today_str} 00:00:00",
                "endTime": f"{today_str} 23:59:59",
                "appId": "wxa5cf43f677b9a059",
                "chooseWay": "1"
            }
            yield scrapy.FormRequest(url=req_url, formdata=req_params, method="GET", callback=self.parse_seat, meta={
                'city_id': v.city_id,
                'store_id': v.store_id,
            })

    def parse_seat(self, response):
        yield self.parse_crawler_item('seat', response)

        body = json.loads(response.body)
        if 'data' not in body:
            print(response.body)
            return
        
        if not body['data']:
            print(response.body)
            return

        for room in body['data']:
            room_id = int(room['roomId'])
            for seat_conf in room['seatSelectionConfigs']:
                item = SeatItem()
                item['city_id'] = response.meta['city_id']
                item['store_id'] = response.meta['store_id']
                item['room_id'] = room_id
                item['seat_id'] = int(seat_conf['seatId'])
                item['space_id'] = int(seat_conf['spaceId'])
                item['space_name'] = seat_conf['spaceName']
                item['coordinate_x'] = float(seat_conf['coordinateX'])
                item['coordinate_y'] = float(seat_conf['coordinateY'])
                item['user_id'] = int(seat_conf.get('userId', 0) or 0)
                item['status'] = int(seat_conf['seatStatus'])
                item['response_time'] = datetime.now()

                yield item

                req_url = f"https://wxa.wangzhizhi.mored.tech/opsli-boot/api/v1/applet/seat/querySeatSpareTime"
                today_str = datetime.now().strftime("%Y-%m-%d")
                req_params = {
                    "storeId": str(item['store_id']),
                    "spaceId": str(item['space_id']),
                    "seatId": str(item["seat_id"]),
                    "studyBeginTime": f"{today_str} 00:00:00",
                    "studyEndTime": f"{today_str} 23:59:59",
                    "appId": "wxa5cf43f677b9a059",
                }
                yield scrapy.FormRequest(url=req_url, formdata=req_params, method="GET", callback=self.parse_seat_occupy, meta={
                    'seat_item': item,
                })

    def parse_seat_occupy(self, response):
        yield self.parse_crawler_item('seat_occupy', response)

        body = json.loads(response.body)
        if 'data' not in body:
            print(response.body)
            return
        
        if not body['data']:
            print(response.body)
            return

        seat_item = response.meta['seat_item']
        user_id = seat_item['user_id']

        now = seat_item['response_time']

        for v in body['data']:
            match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})-(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", v)
            if match:
                start_time_str, end_time_str = match.groups()
                time_format = "%Y-%m-%d %H:%M:%S"
                start_time = datetime.strptime(start_time_str, time_format)
                end_time = datetime.strptime(end_time_str, time_format)
                seat_occupy_item = SeatOccupyItem()

                seat_occupy_item['city_id'] = seat_item['city_id']
                seat_occupy_item['store_id'] = seat_item['store_id']
                seat_occupy_item['seat_id'] = seat_item['seat_id']
                seat_occupy_item['user_id'] = 0
                seat_occupy_item['start_time'] = start_time
                seat_occupy_item['end_time'] = end_time

                if now >= start_time and now <= end_time:
                    seat_occupy_item['user_id'] = user_id

                yield seat_occupy_item