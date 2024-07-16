from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from wangzhizhi_crawler.items import CityItem, StoreItem, SeatItem
from wangzhizhi_crawler.entity.crawler_log import CrawlerLog
from wangzhizhi_crawler.entity.city import City
from wangzhizhi_crawler.entity.store import Store
from wangzhizhi_crawler.entity.seat import Seat
from wangzhizhi_crawler.entity.store_user import StoreUser

import scrapy
import json
from datetime import datetime

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:zzhjrTJ2jRb2G7MS7Zzi93NuERSEpsXE@192.168.89.81:32426/wangzhizhi')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


class WangzhizhiSpider(scrapy.Spider):
    name = "wangzhizhi"

    def start_requests(self):
        req_url = "https://wxa.wangzhizhi.mored.tech/opsli-boot/api/v1/applet/fp/store/org/getStoreArea"
        req_params = {
            "appId": "wxa5cf43f677b9a059"
        }
        yield scrapy.FormRequest(url=req_url, formdata=req_params, method='GET', callback=self.parse_city)

    def parse_city(self, response):
        self.save_crawler_log('city', response)

        body = json.loads(response.body)
        for v in body['data']['areaResults']:
            item = CityItem()
            item['city_id'] = int(v['id'])
            item['name'] = v['areaName']

            self.save_city(item)

            yield item

            req_url = "https://wxa.wangzhizhi.mored.tech/opsli-boot/api/v1/applet/fp/store/org/getStoreBrief"
            req_params = {
                "pageNo": "1",
                "pageSize": "500",
                "cityId": str(item['city_id']),
                "appId": "wxa5cf43f677b9a059"
            }

            yield scrapy.FormRequest(url=req_url, formdata=req_params, method="GET", callback=self.parse_store, meta={
                'city_id': item['city_id'],
            })
    
    def parse_store(self, response):
        self.save_crawler_log('store', response)

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

            self.save_store(item)

            yield item

            req_url = f"https://wxa.wangzhizhi.mored.tech/opsli-boot/api/v1/applet/store/live_situation/query"
            today_str = datetime.now().strftime("%Y-%m-%d")
            req_params = {
                "storeId": str(item['store_id']),
                "startTime": f"{today_str} 00:00:00",
                "endTime": f"{today_str} 23:59:59",
                "appId": "wxa5cf43f677b9a059",
                "chooseWay": "1"
            }
            yield scrapy.FormRequest(url=req_url, formdata=req_params, method="GET", callback=self.parse_seat, meta={
                'city_id': item['city_id'],
                'store_id': item['store_id'],
            })

    def parse_seat(self, response):
        self.save_crawler_log('seat', response)

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

                self.save_seat(item)
                self.save_store_user(item)

                yield item

    def save_crawler_log(self, crawler_type, response):
        with DBSession() as session:
            new_crawler_log = CrawlerLog(
                crawler_type=crawler_type, 
                request_url=response.url,
                response_body=response.body
            )
            session.add(new_crawler_log)
            session.commit()
    
    def save_city(self, item):
        with DBSession() as session:
            city_num = session.query(City).filter(City.city_id == item['city_id']).count()
            if city_num == 0:
                new_city = City(city_id=item['city_id'], name=item['name'], version=0)
                session.add(new_city)
                print(new_city)
            else:
                exist_city = session.query(City).filter(City.city_id == item['city_id']).one()
                exist_city.version = exist_city.version + 1
                session.add(exist_city)
                print(exist_city)

            session.commit()

    def save_store(self, item):
        with DBSession() as session:
            num = session.query(Store).filter(
                and_(
                    Store.city_id == item['city_id'],
                    Store.store_id == item['store_id'],
                )).count()
            if num == 0:
                new_entity = Store(
                    city_id=item['city_id'], 
                    store_id=item['store_id'], 
                    name=item['name'], 
                    lon=item['lon'], 
                    lat=item['lat'], 
                    region=item['region'], 
                    address=item['address'], 
                    status=item['status'], 
                    seat_all=item['seat_all'],
                    seat_current_used=item['seat_current_used'],
                    version=0
                )
                session.add(new_entity)
                print(new_entity)
            else:
                exist_entity = session.query(Store).filter(
                    and_(
                        Store.city_id == item['city_id'],
                        Store.store_id == item['store_id'],
                    )).one()
                exist_entity.status = item['status']
                exist_entity.seat_all = item['seat_all']
                exist_entity.seat_current_used = item['seat_current_used']
                exist_entity.version = exist_entity.version + 1
                session.add(exist_entity)
                print(exist_entity)

            session.commit()

    def save_seat(self, item):
        with DBSession() as session:
            num = session.query(Seat).filter(
                and_(
                    Seat.city_id == item['city_id'],
                    Seat.store_id == item['store_id'],
                    Seat.seat_id == item['seat_id'],
                )).count()
            if num == 0:
                new_entity = Seat(
                    city_id=item['city_id'], 
                    store_id=item['store_id'], 
                    space_id=item['space_id'], 
                    seat_id=item['seat_id'], 
                    space_name=item['space_name'], 
                    coordinate_x=item['coordinate_x'], 
                    coordinate_y=item['coordinate_y'], 
                    status=item['status'], 
                    version=0
                )
                session.add(new_entity)
                print(new_entity)
            else:
                exist_entity = session.query(Seat).filter(
                    and_(
                        Seat.city_id == item['city_id'],
                        Seat.store_id == item['store_id'],
                        Seat.seat_id == item['seat_id'],
                    )).one()
                exist_entity.status = item['status']
                exist_entity.version = exist_entity.version + 1
                session.add(exist_entity)
                print(exist_entity)

            session.commit()
    
    def save_store_user(self, seat_item):
        if seat_item['user_id'] == 0:
            return

        with DBSession() as session:
            city_num = session.query(StoreUser).filter(
                StoreUser.city_id == seat_item['city_id'],
                StoreUser.store_id == seat_item['store_id'],
                StoreUser.user_id == seat_item['user_id'],
            ).count()
            if city_num == 0:
                new_entity = StoreUser(
                    city_id=seat_item['city_id'], 
                    store_id=seat_item['store_id'],
                    user_id=seat_item['user_id'],
                    version=0
                )
                session.add(new_entity)
                print(new_entity)
            else:
                exist_entity = session.query(StoreUser).filter(
                    StoreUser.city_id == seat_item['city_id'],
                    StoreUser.store_id == seat_item['store_id'],
                    StoreUser.user_id == seat_item['user_id']
                ).one()
                exist_entity.version = exist_entity.version + 1
                session.add(exist_entity)
                print(exist_entity)

            session.commit()