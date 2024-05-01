import pymongo
from pymongo import MongoClient, database
import subprocess
import threading
from datetime import datetime, timedelta
import time

# DBName = "CECES327" #Use this to change which Database we're accessing
DBName = "test" #Use this to change which Database we're accessing
connectionURL = "mongodb+srv://kayk:kalynn@ceces327.u6aqfg1.mongodb.net/" #Put your database URL here
# sensorTable = 'Sensor Data'
sensorTable = "traffic data" #Change this to the name of your sensor data table

def QueryToList(query):
	return list(query)  # Convert the MongoDB cursor to a list

def QueryDatabase() -> []:
	global DBName
	global connectionURL
	global currentDBName
	global running
	global filterTime
	global sensorTable
	cluster = None
	client = None
	db = None
	try:
		cluster = connectionURL
		client = MongoClient(cluster)
		db = client[DBName]
		print("Database collections: ", db.list_collection_names())


		sensorTable = db[sensorTable]
		print("Table:", sensorTable)
		
		timeCutOff = datetime.now() - timedelta(minutes=5)

		docs = QueryToList(sensorTable.find({"time":{"$gte":timeCutOff}}))

		if len(docs) == 0:
			print("No recent data found, switching to general data.")
			docs = QueryToList(sensorTable.find({"time":{"$lte":timeCutOff}}))

		sensor_data = []
		for doc in docs:
			payload = doc.get("payload", {})
			if len(payload) > 3:
				keys = list(payload.keys())
				values = list(payload.values())
				sensor_name = keys[3]
				sensor_value = values[3]
				sensor_data.append({"sensor_name": sensor_name, "sensor_value": int(sensor_value)})

		print("Done parsing all data")
		return sensor_data

	except Exception as e:
		print("Please make sure that this machine's IP has access to MongoDB.")
		print("Error:",e)
		exit(0)

