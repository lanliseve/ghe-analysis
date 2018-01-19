# Overview
Purpose is to generate all kinds of GitHub analytics reports automatically, we first export data from GitHub server as json file and then import into database, the report is based on those database.

# Operations
Use this jenkins job: http://16.202.68.117:8081/job/github_export_import/ 
4 parameters:
 - instance: choose the github intance you want to analysis, we may also support all_instsances in the future
 - export script name: a ruby script to export data from github, you should put this file in ruby folder of this repo
 - import script name: your code file to import data into your database, usually it is a python file, put it in python folder of this repo
 - data filename: the filename generated when executing exporting, usually you don't have to change this.

# Servers
 - Jenkins server: server host our jenkins service http://16.202.68.117:8081 hosted in docker container, set up via docker file
 - Ansible server: provide ansible service, hosted on jenkins server, install by execting apt-get install ansible
 - Database server: database instance, mariadb is used currently, hosted on 16.202.71.228:3307 openstack server as docker container
 - GitHub servers: github instances, currently there're 4

# Note
 - Recommand to set ansible home the same as jenkins slave node home
 - Authentiation is done via ssh keys which are stored in sshkeys folder, you need to update/add keys when things changed on server
