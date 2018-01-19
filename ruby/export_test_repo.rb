require 'json'
test_repo_owners = []
repo = Repository.find_by_path("HpTraining6/trainingtest6")
owners = repo.admin_ids.map { |id| User.find_by_id(id).login }
repo1 = {}
repo1[repo.full_name] = owners
test_repo_owners.push repo1

File.open("/tmp/data.json","w") do |f|
 f.write(test_repo_owners.to_json)
 FileUtils.chown 'admin', 'admin', "/tmp/data.json" 
end
