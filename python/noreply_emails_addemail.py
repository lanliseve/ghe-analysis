from pymongo import MongoClient
import json
import sys
import github_restservice

# remove noreply email if it is not the only email
# find email from hpe instance and add it to user who has no email or only have no reply email

NoReply_Key = "users.noreply"

def retrieve_users_to_process(db):
   #ignore suspended users, there're only 2 options for us with suspended users 1. unsuspended them 2. delete them
   return list(db.find({"$and": [ {"suspended": False}, {"login": "feng-zhou"}]}))

def retrieve_all_hpe_users(db):
   return list(db.find({"instance": "hpe"}))

def update_problem_users(db, user, errstr):
   login = user["login"]
   instance = user["instance"]
   emails = user["emails"]
   suspended1 = user["suspended"]
   record = db.find_one({"$and": [ {"login": login}, {"instance": instance}]})
   print("Recording problem login: " + login + " instance: " + instance + " suspended: " + str(suspended1))
   if not record:
      data = {"login":login, "instance":instance, "suspended":suspended1, "emails":emails, "error": errstr}
      db.insert(data)

def find_hpe_emails(hpe_users, username):
   for user in hpe_users:
      if user["login"] == username and user["instance"] == "hpe":
         return user["emails"]
   
   return []

def update_emails_mongo(db, user, emails):
   db.update({"_id": user["_id"]}, {"$set":{"emails": emails}})

def get_problem_users(all_users):
   problem_users = []
   for user in all_users:
      newemails = []
      noreplyemails = []
      for email in user["emails"]:
         if NoReply_Key not in email:
            newemails.append(email)
         else:
            noreplyemails.append(email)
      
      usernoreplyemailscount = len(noreplyemails)
      usernewemailscount = len(newemails)
      if usernoreplyemailscount > 0 or usernewemailscount == 0:
         problem_users.append(user)

   return problem_users

def main():
   # connect to the MongoDB on MongoLab
   # to learn more about MongoLab visit http://www.mongolab.com
   # replace the "" in the line below with your MongoLab connection string
   # you can also use a local MongoDB instance
   mongo_instance = "127.0.0.1:8081"

   # connect to the 'github' database and the 'users' collection
   print("########## Opening connection to MongoDB %s ##########" %(mongo_instance))
   print("Opening connection with MongoDB ...")
   connection = MongoClient(mongo_instance)
   db = connection.github
   dbusers = db.users
   dbproblemusers = db.users_problem

   print("Retrieving users to be processed from database ...")
   all_users = retrieve_users_to_process(dbusers)
   hpe_users = retrieve_all_hpe_users(dbusers)
   #print("Retrieved " + len(all_users) + " users")

   print("Counting problem users before handling ...")
   problem_users = get_problem_users(all_users)
   problemUsersCount = len(problem_users)
   
   print("We have %s problem users before handling" %(problemUsersCount))

   print("Iterating all users to deal with no-reply emails ...")
   count_process = 0
   for user in problem_users:
      login = user["login"]
      instance = user["instance"]
      #print("Begin to process user: " + login + " instance: " + instance)
      newemails = []
      noreplyemails = []
      hpeemails = []
      hpeemailsfound = False
      imptoken = None

      count_process = count_process + 1
      print(str(count_process) + " Begin to process user: " + login + " instance: " + instance + " Suspended: " + str(user["suspended"]))
      
      #search noreply email
      for email in user["emails"]:
         if NoReply_Key not in email:
            newemails.append(email)
         else:
            noreplyemails.append(email)
      
      usernoreplyemailscount = len(noreplyemails)
      usernewemailscount = len(newemails)       
      print("emails analysis finished, no-reply email: " + str(usernoreplyemailscount) + " other emails: " + str(len(newemails)))

      hasnoreply = usernoreplyemailscount > 0
      imptoken = None

      #search email from hpe if no email available, and update github with hpe email if find any
      emailsadded = False
      noreplyremoved = False
      errstr = ""
      try:
         if usernewemailscount == 0 and instance != "hpe":
            hpeemails = find_hpe_emails(hpe_users, login)
            if len(hpeemails) >0:
               print("emails found from hpe")
               imptoken = github_restservice.create_impersonation_github(instance, login)
               hpeemailsfound = True
               newemails = hpeemails
               github_restservice.add_emails_github(instance, login, imptoken, newemails)
               emailsadded = True
            else:
               print("Can NOT find email from hpe")

         #remove noprely email from github
         usernewemailscount = len(newemails)
         if usernewemailscount == 0:
            errstr = "No email available or noereply email is the only email"
            print(errstr)

         #update mongo db of email changes -- 1. noreply removed 2. email found from hpe
         if emailsadded or noreplyremoved:
            #update_emails_mongo(dbusers, user, newemails)  
            print("new emails saved for user")
         print("Process finished for user " + login)
      except Exception, e:
         print "Exception ocurred: %s" % e
         errstr = str(e)
      finally:
         if imptoken != None:
            github_restservice.delete_impersonation_github(instance, login)
         #update problem users who is not processed well 1. has noreply email but cannot be removed 2. has no correct email at all
         if (hasnoreply and noreplyremoved == False) or usernewemailscount == 0:
            update_problem_users(dbproblemusers, user, errstr)

   print("Counting noreply emails after handling ...")
   all_users = retrieve_users_to_process(dbusers)
   problemUsersCount = len(get_problem_users(all_users))
   print("We have %s noreply emails after handling" %(problemUsersCount))

   # close the connection to MongoDB
   connection.close()
   print("Closing connection with MongoDB ...")

main()
