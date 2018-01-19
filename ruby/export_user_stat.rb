require 'json'
all_users = []
User.all.each do |user|
 if user.type=="User"
  user1 = {}
  user1["login"] = user.login
  user1["email"] = user.email
  user1["suspended"] = user.suspended?
  user1["dormant"] = user.dormant?
  user1["site_admin"] = user.site_admin?
  user1["repos"] = user.all_repositories_count
  user1["last_active"] = user.last_active
  user1["raw_login"] = user.raw_login
  user1["gheinstance"] = "hpe"
  user1["created_at"] = user.created_at
  all_users.push user1
 end
end
File.open("all_users_g.json","w") do |f|
f.write(all_users.to_json)
end
