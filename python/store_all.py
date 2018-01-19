import json
import ldap
import sys
import MySQLdb
from pprint import pprint
from datetime import datetime

DateTime_Format = "%Y-%m-%dT%H:%M:%SZ"
_print_debug_info = False

def pardatetime(str1):
    if str1 is not None:
      date_format = DateTime_Format
      if("+" in str1):
        date_format = "%Y-%m-%dT%H:%M:%S+00:00"
        return datetime.strptime(str(str1), date_format)
    else:
      return str1

def open_json(json_file):
    try:
        with open(json_file) as ds:
         data_set = json.load(ds)
        return data_set
    except (OSError, IOError) as e:
        print str(e)
        sys.exit()
def remove_duplicates_in_array(arr):
    return list(set(arr))

def get_database_connection():
    print("Connecting to database")
    db = MySQLdb.connect(host="16.202.71.228", port=3306, user="github", passwd="123456", db="github")
    return db

def clean_orgs(cursor, instance):
    print("About to delete orgs data from database of instance %s " %(instance))

    cursor.execute("delete from orgs where instance = '%s';" %(instance))
    #db.commit()

    cursor.execute("delete from orgs_admins where instance = '%s';" %(instance))
    #db.commit()

    cursor.execute("delete from orgs_teams where instance = '%s';" %(instance))
    #db.commit()

    cursor.execute("delete from orgs_members where instance = '%s';" %(instance))
    #db.commit()

def clean_repos(cursor, instance):
    print("About to delete repos data from database of instance %s " %(instance))

    cursor.execute("delete from repos where instance = '%s';" %(instance))
    #db.commit()

    cursor.execute("delete from repos_admins where instance = '%s';" %(instance))
    #db.commit()

    cursor.execute("delete from repos_teams where instance = '%s';" %(instance))
    #db.commit()

    cursor.execute("delete from repos_members where instance = '%s';" %(instance))
    #db.commit()
    
    cursor.execute("delete from repo_pull_requests where instance = '%s';" %(instance))
    #db.commit()

def clean_users(cursor, instance):
    print("About to delete users data from database of instance %s " %(instance))

    cursor.execute("delete from users where instance = '%s';" %(instance))
    #db.commit()

    cursor.execute("delete from users_emails where instance = '%s';" %(instance))
    #db.commit()

    cursor.execute("delete from users_ldap_emails where instance = '%s';" %(instance))
    #db.commit()

    cursor.execute("delete from app_account_owner where instance = '%s';" %(instance))
    #db.commit()
    
    cursor.execute("delete from user_commit_contributions where instance = '%s';" %(instance))
    #db.commit()

def import_orgs(cursor, data_set, instance):
    clean_orgs(cursor, instance)

    print("About to insert orgs data of instance "+ instance +" with in total " + str(len(data_set["orgs"])) + " records.")
    org_count = 1
    for org in data_set["orgs"]:
        if _print_debug_info:
          print (str(org_count) + " begin to process: ")
          pprint(org)
        org_count = org_count + 1

        instance = org["instance"]
        orgName = org["orgName"]
        orgId = org["orgId"]
        query = ("insert into orgs values (%s, %s, %s);")
        cursor.execute(query,(instance, orgName, orgId))
        #db.commit()
        for owner in remove_duplicates_in_array(org["ownersId"]):
          query = ("insert into orgs_admins values (%s, %s, %s);")
          cursor.execute(query, (instance, orgName, owner))
          #db.commit()
        for team in remove_duplicates_in_array(org["teams"]):
          query = ("insert into orgs_teams values (%s, %s, %s);")
          cursor.execute(query,(instance, orgName, team))
          #db.commit()
        for member in remove_duplicates_in_array(org["all_people"]):
          query = ("insert into orgs_members values (%s, %s, %s);")
          cursor.execute(query,(instance, orgName, member))
          #db.commit()
    
    #db.commit()

def import_repos(cursor, data_set, instance):
    clean_repos(cursor, instance)

    print("About to insert repos data of instance "+ instance +" with in total " + str(len(data_set["repos"])) + " records.")
    repo_count = 1
    for repo in data_set["repos"]:
        if _print_debug_info:
          print (str(repo_count) + " begin to process: ")
          pprint(repo)
        repo_count = repo_count + 1

        instance = repo["instance"]
        repoName = repo["repoName"]
        repoId = repo["repoId"]
        repoFullName = repo["fullName"]
        repoPushAt = ""
        if repo["pushed_at"] is None:
            repoPushAt = repo["pushed_at"]
        elif len(repo["pushed_at"].split(" ")) == 3:
          repoPushAt = repo["pushed_at"].split(" ")[0] + " " + repo["pushed_at"].split(" ")[1]
        else:
          repoPushAt = repo["pushed_at"].split("T")[0] + " " + repo["pushed_at"].split("T")[1].split("Z")[0]
        singlerepoinfo = (instance, repoId, repoName, repoFullName, repo["ownerName"], repo["forked"], repo["owner_type"], pardatetime(repo["create_time"]), repo["visibility"], repo["locked"], repo["lock_reason"], repoPushAt, repo["parent_repo_id"] )
        query = ("insert into repos values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
        cursor.execute(query, singlerepoinfo)
        #db.commit()

        for owner in remove_duplicates_in_array(repo["admins_id"]):
          query = ("insert into repos_admins values (%s, %s, %s);")
          cursor.execute(query, (instance, repoFullName, owner))
          #db.commit()
        for team in remove_duplicates_in_array(repo["teams"]):
          query = ("insert into repos_teams values (%s, %s, %s);")
          cursor.execute(query,(instance, repoFullName, team))
          #db.commit()
        for member in remove_duplicates_in_array(repo["members"]):
          query = ("insert into repos_members values (%s, %s, %s);")
          cursor.execute(query,(instance, repoFullName, member))
          #db.commit()
        for pull_request in repo["pull_requests_info"]:
          query = ("insert into repo_pull_requests values (%s, %s, %s,%s, %s, %s,%s, %s, %s);")
          cursor.execute(query,(instance, pull_request["repo_id"], pull_request["base_repo_id"], pull_request["head_repo_id"], pull_request["base_repo_brance_des"].encode('latin-1', 'ignore'), pull_request["head_repo_brance_des"].encode('latin-1', 'ignore'), pull_request["pull_request_user_id"], pull_request["created_at"].replace("T"," ").replace("Z",""), pull_request["updated_at"].replace("T"," ").replace("Z","")))
          #db.commit()
    #db.commit()

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

def ldap_query_app_find_owner(ownerlist, instance, login, cursor):
  host = 'ldap://ldap.hp.com:389'
  base = 'o=hp.com'
  l = ldap.initialize(host)
  scope = ldap.SCOPE_SUBTREE
  for owner in ownerlist:
    owner_attrs = [ 'hpeSpinCompany', 'uid', 'hpStatus', 'owner', 'member']
    owner_search = l.search_s(base, scope, owner.split(',')[0], owner_attrs)
    if owner_search == []:
      return
    if 'hpStatus' in owner_search[0][1]:
      appquery = ("insert into app_account_owner values(%s,%s,%s,%s,%s)")
      cursor.execute(appquery,(instance, login, owner_search[0][1]["uid"][0], owner_search[0][1]["hpStatus"][0], owner_search[0][1]["hpeSpinCompany"][0]))


def import_users(cursor, data_set, instance):
    clean_users(cursor, instance)

    print("About to insert user data of instance "+ instance +" with in total " + str(len(data_set["users"])) + " records.")
    user_count = 1
    for user in data_set["users"]:
        if _print_debug_info:
          print (str(user_count) + " begin to process: ")
          pprint(user)
        user_count = user_count + 1
        
        instance = user["instance"]
        login = user["login"]
        result = None
        accountType = None
        hpStatus = None
        spinCompany = None
        groupCode = None
        uid = None
        for email in remove_duplicates_in_array(user['emails']):
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
            if _print_debug_info:
              print("ldap info:")
              pprint(result)
            accountType = result["accountType"]
            hpStatus = result["hpStatus"]
            spinCompany = result["hpeSpinCompany"]
            groupCode = result["hpBusinessGroupCode"]
            uid = result["uid"]
            
            if result["email"] != "None":
              newquery = ("insert into users_ldap_emails values (%s, %s, %s)")
              for ldap_email in remove_duplicates_in_array(result["email"]):
                cursor.execute(newquery, (instance, login, ldap_email))
                #db.commit()
            
            if result["accountType"] == "Applications":
              host = 'ldap://ldap.hp.com:389'
              base = 'o=hp.com'
              searchType =  "uid"
              scope = ldap.SCOPE_SUBTREE
              attrs = ['owner']
              l = ldap.initialize(host)
              r = l.search_s(base, scope, "uid="+result["uid"], attrs)
              if "owner" in r[0][1]:
                ldap_query_app_find_owner(remove_duplicates_in_array(r[0][1]["owner"]),instance,login,cursor)
        
        singleuserinfo = (instance,user["userId"], login,  user["primary"], user["suspended"], user["dormant"], user["site_admin"],
             user["last_active"],  pardatetime(user["created_at"]), accountType, hpStatus, spinCompany, groupCode, uid, pardatetime(user["last_web_session_time"]), pardatetime(user["last_audit_log_entry_time"]), pardatetime(user["last_dashboard_event_time"]), pardatetime(user["last_repo_star_time"]), pardatetime(user["last_repo_watch_time"]))
        query = ("insert into users values (  %s, %s, %s, %s, %s,   %s, %s, %s, %s,   %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s);")
        cursor.execute(query, singleuserinfo)
        #db.commit()

        for email in remove_duplicates_in_array(user["emails"]):
          query = ("insert into users_emails values (%s, %s, %s);")
          cursor.execute(query,(instance, login, email))
        for commitInfo in user["commit_info"]:
          query = ("insert into user_commit_contributions values (%s, %s, %s, %s);")
          cursor.execute(query,(instance, login, commitInfo["commit_date"], commitInfo["repo_id"] ))
          #db.commit()
    #db.commit()

def process(cursor, data_set, instance):
    import_orgs(cursor, data_set, instance)
    import_repos(cursor, data_set, instance)
    import_users(cursor, data_set, instance)

def main():
      json_file = sys.argv[1] 
      instance = sys.argv[2]
      if sys.argv[3] == "false":
        _print_debug_info = False
      else:
        _print_debug_info = True

      data_set = open_json(json_file)
      db = get_database_connection()
      cursor = db.cursor()
      process(cursor, data_set, instance)
      db.commit()
      cursor.close()
      db.close()
      print("Closing connection with Mariadb ...")

main()
