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
   attrs = ['hpBusinessGroupCode','hpeSpinCompany']
   l = ldap.initialize(host)
   # Try to find as "uid", if not try to search by "mail"
   r = l.search_s(base, scope, "uid="+search, attrs)
   if not r:
      r = l.search_s(base, scope, "mail="+search, attrs)
      searchType =  "email"

   if not r:
      return ("NONE","NONE","N/A")

   if "hpeSpinCompany" in r[0][1] and "hpBusinessGroupCode" in r[0][1]:
      return (r[0][1]["hpBusinessGroupCode"][0],r[0][1]["hpeSpinCompany"][0], searchType)
   elif "hpeSpinCompany" in r[0][1] :
      return ("NONE",r[0][1]["hpeSpinCompany"][0], searchType)
   elif "hpBusinessGroupCode" in r[0][1]:
      return (r[0][1]["hpBusinessGroupCode"][0],"NONE",searchType)
   else:
       return ("NONE","NONE","N/A")

def main():
   # connect to the MongoDB on MongoLab
   # to learn more about MongoLab visit http://www.mongolab.com
   # replace the "" in the line below with your MongoLab connection string
   # you can also use a local MongoDB instance
   mongo_instance = "127.0.0.1"
   connection = MongoClient(mongo_instance)
   # connect to the 'github' database and the 'users' collection
   db = connection.github.users
   db_alignments = connection.github.alignments
   results = db.find()
   #print results


   print "########## Opening connection to MongoDB %s ##########" %(mongo_instance)
   for record in results:
      if ("alignment" in record):
         print record
      alignment = "NONE"
      spinco = "NONE"
      ownerEmail = "NONE"
      searchtype = "N/A"
      for email in record["emails"]:
         ownerEmail = email
         (alignment,spinco,searchtype) = ldap_query_bu(str(email))
         if spinco != "NONE":
            ownerEmail = email
            break
      db_alignments.insert({"name": str(record["name"]), "alignment": alignment,"spinco":spinco, "email": ownerEmail, "Type": searchtype})
   print "Closing connection with MongoDB ..."
   connection.close()


main()
