import threading
import pymongo
import logging
from scrapy import signals

from douban.items.movie_item import MovieItem

logger = logging.getLogger(__name__)


class MongoPipeline(object):
    lock = threading.Lock()

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_uri)
        logger.info('Mongodb connected.')
        self.db = self.client[self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )
        crawler.signals.connect(pipeline.disconnect, signals.engine_stopped)
        return pipeline

    def disconnect(self):
        self.client.close()
        logger.info('Mongodb disconnected.')

    def process_item(self, item, spider):
        with self.lock:
            self.db[item.Meta.db_collection_name]\
                .find_one_and_update({'id': item['id']}, {'$set': dict(item)}, upsert=True)
        return item



