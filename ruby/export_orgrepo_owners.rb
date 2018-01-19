require 'json'
org_repo_owners = {}
Repository.all.each do |repo|
  if repo.user.instance_of? Organization
    owners = repo.admin_ids.map { |id| User.find_by_id(id).login }
    org_repo_owners[repo.full_name] = owners
  end
end
File.open("org_repo_owners.json","w") do |f|
f.write(org_repo_owners.to_json)
end
