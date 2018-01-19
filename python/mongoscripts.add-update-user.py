from pymongo import MongoClient
import json
import sys

def open_json(json_file):
   try:
      with open(json_file) as ds:
         data_set = json.load(ds)
      return data_set
   except (OSError, IOError) as e:
      print str(e)
      sys.exit()

def main():
   # connect to the MongoDB on MongoLab
   # to learn more about MongoLab visit http://www.mongolab.com
   # replace the "" in the line below with your MongoLab connection string
   # you can also use a local MongoDB instance
   mongo_instance = "127.0.0.1"
   json_file = "/partner/user_emails_20170614.json"
   print "########## Opening connection to MongoDB %s ##########" %(mongo_instance)
   connection = MongoClient(mongo_instance)
   # connect to the 'github' database and the 'users' collection
   db = connection.github.users
   data_set = open_json(json_file)
   for user, emails in data_set.iteritems():
      record = db.find_one({'name': str(user)})
      if record:
         if record["emails"] == emails:
           continue
         if record["emails"]:
           emails.extend(record["emails"])

         db.update({"name": str(record["name"])}, {"$set":{"emails": emails}})
      else:
         record = {"name": str(user), "emails": emails}
         # insert the record
         #print "Inserting user %s ..." %(str(user))
         db.insert(record)

   # close the connection to MongoDB
   connection.close()
   print "Closing connection with MongoDB ..."

main()
