from pymongo import MongoClient
import sys
import ldap

def ldap_query_bu(search):
   # HPE LDAP
   host = 'ldap://ldap.hp.com:389'
   base = 'o=hp.com'
   searchType =  "uid"
   scope = ldap.SCOPE_SUBTREE
   # Attributes requested
   attrs = ['hpBusinessGroupCode', 'spinco']
   l = ldap.initialize(host)
   # Try to find as "uid", if not try to search by "mail"
   r = l.search_s(base, scope, "uid="+search, attrs)
   if not r:
      r = l.search_s(base, scope, "mail="+search, attrs)
      searchType =  "email"

   if not r:
      return ("NONE","N/A")

   if "spinco" in r[0][1]:
      return (r[0][1]["spinco"][0])
   else:
      return ("NONE","N/A")

def main():
   # connect to the MongoDB on MongoLab
   # to learn more about MongoLab visit http://www.mongolab.com
   # replace the "" in the line below with your MongoLab connection string
   # you can also use a local MongoDB instance
   mongo_instance = "127.0.0.1"
   connection = MongoClient(mongo_instance)
   # connect to the 'github' database and the 'users' collection
   db_alignments = connection.github.alignments
   results = db_alignments.find()
   #print results


   print "########## Opening connection to MongoDB %s ##########" %(mongo_instance)
   for record in results:
      spinco = "NONE"
	  print "updating record %s" %str(record["name"])
	  if record["email"]:
	     spinco = ldap_query_bu(str(record["email"]))
         db_alignments.update({"name": str(record["name"])}, {"$set":{"spinco": str(spinco)}})
   print "Closing connection with MongoDB ..."
   connection.close()


main()
