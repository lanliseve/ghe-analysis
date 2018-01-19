import json
import sys
import MySQLdb

def open_json(json_file):
   try:
      with open(json_file) as ds:
         data_set = json.load(ds)
      return data_set
   except (OSError, IOError) as e:
      print str(e)
      sys.exit()

json_file = "repo_info.json"
data_set = open_json(json_file)
db = MySQLdb.connect("localhost", "root", "123456", "github")
cursor = db.cursor()
   
for login, storedata in data_set.iteritems():
  query = ("select count(*) from repos") 

  cursor.execute(query)
  data = cursor.fetchone()
  repoid = int(data[0]) + 1
  singlerepoinfo = (repoid, storedata["instance"], storedata["repoName"], storedata["ownerName"], 
    storedata["forked"], storedata["owner_type"], storedata["create_time"], storedata["visibility"])
  query = ("insert into repos values (%s, %s, %s, %s, %s, %s, %s, %s);")
  cursor.execute(query, singlerepoinfo)
  db.commit()
  for owner in storedata["admins"]:
    query = ("insert into repos_admins values (%s, %s);")
    cursor.execute(query,(repoid, owner))
    db.commit()
  for team in storedata["teams"]:
    query = ("insert into repos_teams values (%s, %s);")
    cursor.execute(query,(repoid, team))
    db.commit()
  for member in storedata["members"]:
    query = ("insert into repos_members values (%s, %s);")
    cursor.execute(query,(repoid, member))
    db.commit()
cursor.close()
db.close()
