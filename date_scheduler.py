import pymongo
from datetime import datetime, timedelta
from search_cian import crawler

def updating_crawler(page_id):
	crawler(page_id)
	myquery = { "_id":  page_id}
	newvalues = { "$set": { 'seen_as_old': True } }
	mycol.update_one(myquery, newvalues)
	print('updated', page_id)


myclient = pymongo.MongoClient('localhost', 27017, maxPoolSize=200)
db = myclient.flats
# выбираем коллекцию документов
mycol = db.coll
past = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
print('past = ', past)
import multiprocessing as mp
num_of_cores = 1#mp.cpu_count()-2
print('Start execution with ' + str(num_of_cores) + ' cores.')
pool = mp.Pool(num_of_cores)
for old_dict in mycol.find({ 'date_of_adding_to_db': {"$lt": past}, 'seen_as_old': { "$exists": False } , 'visitors': {"$ne": None}}):
	try:
		pool.apply_async(updating_crawler, args=(old_dict['id']))
		# updating_crawler(old_dict['id'])
		# myquery = { "_id":  old_dict['_id']}
		# newvalues = { "$set": { 'seen_as_old': True } }
		# mycol.update_one(myquery, newvalues)
		# print('updated', old_dict['id'])
	except:
		print('error')
		myclient.close()
		break
pool.close()
pool.join()
myclient.close()