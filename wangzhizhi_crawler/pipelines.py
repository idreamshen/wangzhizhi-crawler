# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import and_
from wangzhizhi_crawler.items import CrawlerItem, CityItem, StoreItem, SeatItem, SeatOccupyItem
from wangzhizhi_crawler.entity.crawler_log import CrawlerLog
from wangzhizhi_crawler.entity.city import City
from wangzhizhi_crawler.entity.store import Store
from wangzhizhi_crawler.entity.store_seat_stats import StoreSeatStats
from wangzhizhi_crawler.entity.store_user import StoreUser
from wangzhizhi_crawler.entity.seat import Seat
from wangzhizhi_crawler.entity.seat_occupy import SeatOccupy
from wangzhizhi_crawler.db import DBSession


class WangzhizhiPipeline:
    def process_item(self, item, spider):

        if isinstance(item, SeatOccupyItem):
            print(SeatOccupyItem)

        return item
    
class CrawlerItemPipeline:
    def process_item(self, item, spider):

        if not isinstance(item, CrawlerItem):
            return item

        with DBSession() as session:
            new_crawler_log = CrawlerLog(
                crawler_type = item["crawler_type"], 
                request_url = item["request_url"],
                response_body = item["response_body"]
            )
            session.add(new_crawler_log)
            session.commit()
            print(new_crawler_log)

        return item

class CityItemPipeline:
    def process_item(self, item, spider):
        if not isinstance(item, CityItem):
            return item

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
        
        return item

class StoreItemPipeline:
    def process_item(self, item, spider):
        if not isinstance(item, StoreItem):
            return item

        self.save_store(item)
        self.save_store_seat_stats(item)
        return item
    
    def save_store(self, item):
        with DBSession() as session:
            num = session.query(Store).filter(
                and_(
                    Store.city_id == item['city_id'],
                    Store.store_id == item['store_id'],
                )).count()
            if num == 0:
                new_entity = Store(
                    city_id = item['city_id'], 
                    store_id = item['store_id'], 
                    name = item['name'], 
                    lon = item['lon'], 
                    lat = item['lat'], 
                    region = item['region'], 
                    address = item['address'], 
                    status = item['status'], 
                    seat_all = item['seat_all'],
                    seat_current_used = item['seat_current_used'],
                    version = 0
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

    def save_store_seat_stats(self, item):
        with DBSession() as session:
            
            new_entity = StoreSeatStats(
                city_id = item['city_id'], 
                store_id = item['store_id'], 
                seat_all = item['seat_all'],
                seat_current_used = item['seat_current_used'],
            )
            session.add(new_entity)
            print(new_entity)
            
            session.commit()

class SeatItemPipeline:
    def process_item(self, item, spider):

        if not isinstance(item, SeatItem):
            return item        

        self.save_seat(item)
        self.save_store_user(item)

        return item

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
    
    def save_store_user(self, item):
        if item['user_id'] == 0:
            return

        with DBSession() as session:
            city_num = session.query(StoreUser).filter(
                StoreUser.city_id == item['city_id'],
                StoreUser.store_id == item['store_id'],
                StoreUser.user_id == item['user_id'],
            ).count()
            if city_num == 0:
                new_entity = StoreUser(
                    city_id=item['city_id'], 
                    store_id=item['store_id'],
                    user_id=item['user_id'],
                    version=0
                )
                session.add(new_entity)
                print(new_entity)
            else:
                exist_entity = session.query(StoreUser).filter(
                    StoreUser.city_id == item['city_id'],
                    StoreUser.store_id == item['store_id'],
                    StoreUser.user_id == item['user_id']
                ).one()
                exist_entity.version = exist_entity.version + 1
                session.add(exist_entity)
                print(exist_entity)

            session.commit()

class SeatOccupyItemPipeline:
    def process_item(self, item, spider):
        if not isinstance(item, SeatOccupyItem):
            return item

        self.save_seat_occupy(item)
        return item

    def save_seat_occupy(self, item):
         with DBSession() as session:
            seat_occupy_count = session.query(SeatOccupy).filter(
                SeatOccupy.city_id == item['city_id'],
                SeatOccupy.store_id == item['store_id'],
                SeatOccupy.seat_id == item['seat_id'],
                SeatOccupy.start_time == item['start_time'],
                SeatOccupy.end_time == item['end_time']
            ).count()

            if seat_occupy_count == 0:
                new_entity = SeatOccupy(
                    city_id = item['city_id'], 
                    store_id = item['store_id'],
                    seat_id = item['seat_id'],
                    user_id = item['user_id'],
                    start_time = item['start_time'],
                    end_time = item['end_time']
                )
                session.add(new_entity)
                print(new_entity)
            else:
                seat_occupies = session.query(SeatOccupy).filter(
                    SeatOccupy.city_id == item['city_id'],
                    SeatOccupy.store_id == item['store_id'],
                    SeatOccupy.seat_id == item['seat_id'],
                    SeatOccupy.start_time == item['start_time'],
                    SeatOccupy.end_time == item['end_time']
                ).all()

                for v in seat_occupies:
                    if item['user_id'] > 0 and v.user_id == 0:
                        v.user_id = item['user_id']
                        session.add(v)
            
            session.commit()
