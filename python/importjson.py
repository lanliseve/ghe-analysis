from pymongo import MongoClient
import json
import sys

def main():
   # connect to the MongoDB on MongoLab
   # to learn more about MongoLab visit http://www.mongolab.com
   # replace the "" in the line below with your MongoLab connection string
   # you can also use a local MongoDB instance
   mongo_instance = "127.0.0.1:8081"

   print("########## Opening connection to MongoDB %s ##########" %(mongo_instance))
   connection = MongoClient(mongo_instance)
   # connect to the 'github' database and the 'users' collection
   schema = sys.argv[1]
   db = connection.github.test_automation
   
   #db.drop()

   jsonpath = sys.argv[1]
   print("data path:" + jsonpath)
   with open(jsonpath) as ds:
    data_set = json.load(ds)
   result = db.insert_many(data_set)

   # close the connection to MongoDB
   connection.close()
   print("Closing connection with MongoDB ...")

main()
