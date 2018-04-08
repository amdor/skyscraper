import atexit
from pymongo import MongoClient

from skyscraper.utils.constants import MONGO_URL, DB_NAME, CAR_DETAILS

dbClient = MongoClient(MONGO_URL)
db = dbClient[DB_NAME]
atexit.register(dbClient.close)


class DatabaseService:
	def __init__(self):
		pass

	@staticmethod
	def save_car_data(id, data_arr):
		db[CAR_DETAILS].replace_one({id: {"$exists": True}}, {id: data_arr}, upsert=True)

	@staticmethod
	def get_car_data(id):
		return db[CAR_DETAILS].find_one({id: {"$exists": True}})
