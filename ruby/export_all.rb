require 'json'
#partner = "partner-github-hpe-com\n"
hostinfo = `hostname`
instance = "not set"
if hostinfo.include? "partner"
    instance = "partner"
elsif hostinfo.include? "softwaregrp"
    instance = "seattle"
elsif hostinfo.include? "e4a0012g"
    instance = "dxc"
elsif hostinfo.include? "github-hpe-com-primary"
    instance = "hpe"
else 
    raise Exception.new("wrong hostname, script terminated")
end

all_info = {}

org_info = []
Organization.all.each do |org|
    single_org_members = {}
    single_org_members['instance'] = instance
    members = []
    teams = []
    single_org_members['ownersId'] = org.admin_ids
    org.people.each do |k| members.append(k.login) end
    org.teams.each do |k| teams.append(k.name) end
    single_org_members['all_people'] = members
    single_org_members['teams'] = teams
    single_org_members['orgName'] = org.login
    single_org_members['orgId'] =  org.id
    org_info.push single_org_members
end
all_info["orgs"] = org_info

repo_info = []
Repository.all.each do |repo|
    single_repo = {}
    single_repo['repoId'] = repo.id
    single_repo['instance'] = instance
    single_repo['admins_id'] = repo.admin_ids
    single_repo['teams'] = repo.teams.map { |m| m.name }
    single_repo['repoName'] = repo.name
    single_repo['ownerName'] = repo.user.login
    single_repo['members'] = repo.all_members_and_owners.map { |n| n.login }
    single_repo['forked'] = repo.fork?
    single_repo['owner_type'] = repo.user.type
    single_repo['create_time'] = repo.created_at
    single_repo['visibility'] = repo.visibility
    single_repo['fullName'] = repo.full_name
    single_repo['locked'] = repo.locked?
    single_repo['lock_reason'] = repo.lock_reason
    single_repo['pushed_at'] = repo.pushed_at
    single_repo['pull_requests_info'] = []
    single_repo['parent_repo_id'] = repo.parent_id
    repo.pull_requests.each do |request_info|
      single_request_info = {}
      single_request_info["repo_id"] = request_info.repository_id
      single_request_info["base_repo_id"] = request_info.base_repository_id
      single_request_info["head_repo_id"] = request_info.head_repository_id
      single_request_info["pull_request_user_id"] = request_info.user_id
      single_request_info["base_repo_brance_des"] = request_info.base_ref
      single_request_info["head_repo_brance_des"] = request_info.head_ref
      single_request_info["created_at"] = request_info.created_at
      single_request_info["updated_at"] = request_info.updated_at
      single_repo['pull_requests_info'].push single_request_info
    end
    repo_info.push single_repo
end
all_info["repos"] = repo_info

user_info = []
User.all.each do |user|
  if user.type != "User"
    next
  end
  storedata = {}
  storedata["userId"] = user.id
  storedata["login"] = user.login
  storedata["instance"] = instance
  #storedata["ssh_keys"] = user.public_key_ids.count
  #storedata["org_memberships"] = user.organizations.count
  storedata["suspended"] = user.suspended?
  storedata["dormant"] = user.dormant?
  storedata["site_admin"] = user.site_admin?
  #storedata["repos"] = user.all_repositories_count
  storedata["last_active"] = user.last_active
  #storedata["raw_login"] = user.raw_login
  storedata["created_at"] = user.created_at
  storedata['emails'] = []
  storedata['commit_info'] = []
  storedata['primary'] = user.email 
  storedata['last_web_session_time'] = user.last_web_session_time
  storedata['last_dashboard_event_time'] = user.last_dashboard_event_time
  storedata['last_audit_log_entry_time'] = user.last_audit_log_entry_time
  storedata['last_repo_star_time'] = user.last_repo_star_time
  storedata['last_repo_watch_time'] = user.last_repo_watch_time
  user.commit_contributions.each do |commit_info|
      single_commit_info = {}
      single_commit_info["repo_id"] = commit_info.repository_id
      single_commit_info["commit_date"] = commit_info.committed_date
      storedata['commit_info'].push single_commit_info
  end
  user.emails.each do |email|
    storedata['emails'].push email.email
  end
  user_info.push storedata
end
all_info["users"] = user_info

File.open("/tmp/data.json","w") do |f|
  f.write(all_info.to_json)
end
