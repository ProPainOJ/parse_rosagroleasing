import pymongo
import time


class DB_Mongo:

    def __init__(self, list_dict, host="localhost", port="27017", password=None):
        self.list_dict = list_dict
        self.host = host
        self.port = port
        self.password = password
        self.db = None
        self.client = None
        self.collection_name = None

    def connection(self):
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017")
        except:
            while self.client is not None:
                print("    [ERROR] Ошибка доступа к серверу MongoDB!")
                self.client = pymongo.MongoClient("mongodb://localhost:27017")
                time.sleep(5)
                
        self.db = self.client.new_db_for_rosagroleazing # Название бд для записи
        coll_name = str(self.list_dict['Категория'])
        collection = self.db[coll_name]
        collection.insert_one(self.list_dict)
