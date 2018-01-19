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

json_file = "org_info.json"
data_set = open_json(json_file)
db = MySQLdb.connect("localhost", "root", "123456", "github")
cursor = db.cursor()
   
for login, storedata in data_set.iteritems():
  query = ("select count(*) from orgs") 

  cursor.execute(query)
  data = cursor.fetchone()
  orgid = int(data[0]) + 1
  instance = storedata["instance"]
  orgName = storedata["orgName"]
  query = ("insert into orgs values (%s, %s, %s);")
  cursor.execute(query,(orgid, orgName, instance))
  db.commit()
  for owner in storedata["owners"]:
    query = ("insert into orgs_admins values (%s, %s);")
    cursor.execute(query,(orgid, owner))
    db.commit()
  for team in storedata["teams"]:
    query = ("insert into orgs_teams values (%s, %s);")
    cursor.execute(query,(orgid, team))
    db.commit()
  for member in storedata["all_people"]:
    query = ("insert into orgs_members values (%s, %s);")
    cursor.execute(query,(orgid, member))
    db.commit()
cursor.close()
db.close()
