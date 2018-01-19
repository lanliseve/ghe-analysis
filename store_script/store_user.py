import json
import ldap
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

def ldap_query_bu(search):
  host = 'ldap://ldap.hp.com:389'
  base = 'o=hp.com'
  searchType =  "uid"
  scope = ldap.SCOPE_SUBTREE
  # Attributes requested
  attrs = ['hpBusinessGroupCode', 'hpeSpinCompany', 'uid', 'mail', 'hpStatus']
  l = ldap.initialize(host)
  # Try to find as "uid", if not try to search by "mail"
  r = l.search_s(base, scope, "uid="+search, attrs)
  if not r:
     r = l.search_s(base, scope, "mail="+search, attrs)
     searchType =  "email"
  if not r:
    return None
  result = {}
  result["hpBusinessGroupCode"] = "None"
  result["hpeSpinCompany"] = "None"
  result["uid"] = "None"
  result["email"] = "None"
  result["accountType"] = "None"
  result["hpStatus"] = "None"
  result["accountType"] = r[0][0].split(',')[1].split('=')[1]
  if "uid" in r[0][1]:
    result["uid"] = r[0][1]["uid"][0]
  if  result["accountType"] == "Applications":
    return result
  if "hpBusinessGroupCode" not in r[0][1] and "hpeSpinCompany" not in r[0][1]:
    return None
  if "hpBusinessGroupCode" in r[0][1]:
    result["hpBusinessGroupCode"] = r[0][1]["hpBusinessGroupCode"][0]
  if "hpeSpinCompany" in r[0][1]:
    result["hpeSpinCompany"] = r[0][1]["hpeSpinCompany"][0] 
  if "mail" in r[0][1]:
    result["email"] = r[0][1]["mail"] 
  if "hpStatus" in r[0][1]:
    result["hpStatus"] = r[0][1]["hpStatus"][0]
    if len(r[0][1]["hpStatus"]) > 1:
     print result["uid"]
  
  return result

def ldap_query_app(search):
  host = 'ldap://ldap.hp.com:389'
  base = 'o=hp.com'
  searchType =  "uid"
  scope = ldap.SCOPE_SUBTREE
  # Attributes requested
  attrs = ['uid']
  l = ldap.initialize(host)
  # Try to find as "uid", if not try to search by "mail"
  r = l.search_s(base, scope, "uid="+search, attrs)
  if not r:
    return None
  result = {}
  result["hpBusinessGroupCode"] = "None"
  result["hpeSpinCompany"] = "None"
  result["uid"] = search
  result["email"] = "None"
  result["accountType"] = "Applications"
  result["hpStatus"] = "None"

  return result

def ldap_query_app_find_owner(ownerlist, userid, cursor, db):
  host = 'ldap://ldap.hp.com:389'
  base = 'o=hp.com'
  l = ldap.initialize(host)
  for owner in ownerlist:
    owner_attrs = [ 'hpeSpinCompany', 'uid', 'hpStatus', 'owner', 'member']
    owner_search = l.search_s(base, scope, owner.split(',')[0], owner_attrs)
    if 'hpStatus' in owner_search[0][1]:
      appquery = ("insert into app_account_owner_info values(%s,%s,%s,%s)")
      cursor.execute(appquery,(userid, owner_search[0][1]["hpStatus"][0], owner_search[0][1]["hpeSpinCompany"][0],owner_search[0][1]["uid"][0]))
      db.commit()

json_file = "users_info.json"
data_set = open_json(json_file)
db = MySQLdb.connect("localhost", "root", "123456", "github")
cursor = db.cursor()
   
for login, storedata in data_set.iteritems():
  query = ("select count(*) from users") 
  cursor.execute(query)
  data = cursor.fetchone()
  userid = int(data[0]) + 1
  result = None
  for email in storedata['emails']:
    result = ldap_query_bu(str(email))
    if result is not None:
      break
    else:
      result1 = ldap_query_app(str(login))
      result2 = ldap_query_app(str(login).replace("-","_"))
      result3 = ldap_query_app(str(login).replace("-","."))
      result = (result1 or result2) or result3
      if result is not None:
        break
  if result is not None:
    singleuserinfo = (userid, storedata["instance"], login, storedata["ssh_keys"], storedata["org_memberships"], 
      storedata["primary"], storedata["suspended"], storedata["dormant"], storedata["site_admin"],
      storedata["repos"], storedata["last_active"], storedata["raw_login"], storedata["created_at"],
      result["accountType"], result["hpStatus"], result["hpeSpinCompany"],result["hpBusinessGroupCode"],result["uid"])
    newquery = ("insert into users_ldap_emails values (%s, %s)")
    for ldap_email in result["email"]:
      cursor.execute(newquery,(userid, ldap_email))
      db.commit()
    if result["accountType"] == "Applications":
      host = 'ldap://ldap.hp.com:389'
      base = 'o=hp.com'
      searchType =  "uid"
      scope = ldap.SCOPE_SUBTREE
      attrs = ['owner']
      l = ldap.initialize(host)
      r = l.search_s(base, scope, "uid="+result["uid"], attrs)
      ldap_query_app_find_owner(r[0][1]["owner"],userid,cursor,db)
  else:
    singleuserinfo = (userid, storedata["instance"], login, storedata["ssh_keys"], storedata["org_memberships"], 
      storedata["primary"], storedata["suspended"], storedata["dormant"], storedata["site_admin"],
      storedata["repos"], storedata["last_active"], storedata["raw_login"], storedata["created_at"],
      "None", "None","None","None","None" )
    
  query = ("insert into users values (%s, %s, %s, %s,   %s, %s, %s, %s,   %s, %s, %s, %s,   %s, %s, %s, %s, %s, %s);")
  cursor.execute(query, singleuserinfo)
  db.commit()
  for email in storedata["emails"]:
    query = ("insert into users_emails values (%s, %s);")
    cursor.execute(query,(userid, email))
    db.commit()
cursor.close()
db.close()


