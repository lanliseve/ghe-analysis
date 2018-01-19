from pymongo import MongoClient
import json
import sys
import github_restservice

# remove noreply email if it is not the only email
# find email from hpe instance and add it to user who has no email or only have no reply email

NoReply_Key = "@users.noreply."

def retrieve_users_to_process(db):
   #ignore suspended users, there're only 2 options for us with suspended users 1. unsuspended them 2. delete them
   #return list(db.find({"$and": [ {"suspended": False}, {"instance": "seattle"}]}))
   return list(db.find({"suspended": False}))

def retrieve_all_users(db):
   return list(db.find())
def find_duplicate_user(all_users, instance, originalemail):
   targetuser = None   
   for user in all_users:
      if user["instance"] == instance:
         for email in user["emails"]:
            if email == originalemail:
               targetuser = user
               break;
   
   return targetuser

def update_problem_users(db, user, errstr, all_users, originalemails):
   login = user["login"]
   instance = user["instance"]
   emails = user["emails"]
   suspended1 = user["suspended"]
   record = db.find_one({"$and": [ {"login": login}, {"instance": instance}]})
   print("Recording problem login: " + login + " instance: " + instance + " suspended: " + str(suspended1))
   if not record:
      originalemail = ""
      emailoccubied = False
      duplicateusername = ""
      if "422 Client Error: Unprocessable Entity for url" in errstr:
         for email in originalemails:
            if NoReply_Key not in email:
               originalemail = email
               break

      if originalemail != "":
         #find user with the same email in the same instance but with different github username
         dpuser = find_duplicate_user(all_users, instance, originalemail)
         if dpuser:
            emailoccubied = True
            duplicateusername = dpuser["login"] 

      data = {"login":login, "instance":instance, "suspended":suspended1, "emails":emails, "error": errstr, "emailoccubied": emailoccubied, "emailoccubiedby": duplicateusername, "originalemails": originalemails}
      db.insert(data)

def find_original_emails(all_users, instance, username):
   for user in all_users:
      if user["login"] == username and user["instance"] == instance:
         for email in user["emails"]:
            if NoReply_Key not in email:
               return user["emails"]         
   
   return []

def update_emails_mongo(db, user, emails):
   db.update({"_id": user["_id"]}, {"$set":{"emails": emails}})

def get_problem_users(users_to_process):
   problem_users = []
   for user in users_to_process:
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
def get_database_connection():
   # connect to the MongoDB on MongoLab
   # to learn more about MongoLab visit http://www.mongolab.com
   # replace the "" in the line below with your MongoLab connection string
   # you can also use a local MongoDB instance
   mongo_instance = "127.0.0.1:8081"

   # connect to the 'github' database and the 'users' collection
   print("########## Opening connection to MongoDB %s ##########" %(mongo_instance))
   print("Opening connection with MongoDB ...")
   connection = MongoClient(mongo_instance)
   return connection

def process(connection):
   db = connection.github
   dbusers = db.users
   dbproblemusers = db.users_problem

   print("Retrieving users to be processed from database ...")
   users_to_process = retrieve_users_to_process(dbusers)
   all_users = retrieve_all_users(dbusers)

   print("Counting problem users before handling ...")
   problem_users = get_problem_users(users_to_process)
   problemUsersCount = len(problem_users)
   
   print("We have %s problem users before handling" %(problemUsersCount))

   print("Iterating all users to deal with no-reply emails ...")
   count_process = 0
   for user in problem_users:
      login = user["login"]
      instance = user["instance"]
      originalinstance = None
      #print("Begin to process user: " + login + " instance: " + instance)
      newemails = []
      noreplyemails = []
      originalemails = []
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
         if usernewemailscount == 0:
            #search email from original/migrated from instance for users who only have a noreply email
            originalinstance = "hpe"
            if hasnoreply:            
               index = noreplyemails[0].index(NoReply_Key) + len(NoReply_Key)
               originalhost = noreplyemails[0][index:]
               originalinstance = github_restservice.get_instance_by_hostname(originalhost)
            print("searching emails from original instance: " + originalinstance) 
            originalemails = find_original_emails(all_users, originalinstance, login)
            if len(originalemails) >0:
               print("emails found from original instance")
               imptoken = github_restservice.create_impersonation_github(instance, login)
               newemails = originalemails
               github_restservice.add_emails_github(instance, login, imptoken, newemails)
               emailsadded = True
            else:
               print("Can NOT find email from original instance")

         #remove noprely email from github
         usernewemailscount = len(newemails)
         if usernewemailscount == 0:
            errstr = "No email available or noereply email is the only email"
            print(errstr)
         elif hasnoreply:
            if(imptoken == None):
               imptoken = github_restservice.create_impersonation_github(instance, login)
            github_restservice.remove_emails_github(instance, login, imptoken, noreplyemails)
            noreplyremoved = True

         #update mongo db of email changes -- 1. noreply removed 2. email found from hpe
         if emailsadded or noreplyremoved:
            update_emails_mongo(dbusers, user, newemails)  
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
            update_problem_users(dbproblemusers, user, errstr, all_users, originalemails)

   print("Counting noreply emails after handling ...")
   users_to_process = retrieve_users_to_process(dbusers)
   problemUsersCount = len(get_problem_users(users_to_process))
   print("We have %s noreply emails after handling" %(problemUsersCount))

def main():
   try:
      connection = get_database_connection()
      process(connection)
   finally:
      # close the connection to MongoDB
      connection.close()
      print("Closing connection with MongoDB ...")

main()
