#!/usr/bin/env python3
#
# So the idea is to check for all of the repos that I own/clone/participate in and mirror them. 
#
# foreach repo.
#    if repo is not mirrored
#         create a mirror
#     else 
#         update the mirror
#
# add the entry into /srv/git/repolist for cgit 
#
#  repo.url=git@github.com/feurig/blahblah.git
#  repo.name=wcm
#  repo.owner=feurig
#  repo.path=/home/git/repositories/blahblah.git
#  repo.desc= blah blah blah
#
# Consider sorting by prefix and making group entries

import os
import subprocess
from github import Github
from github import Auth
from dotenv import load_dotenv
import tempfile


load_dotenv()
    
auth_token = os.environ["AUTH_TOKEN"]

def mygithub() :
    auth = Auth.Token(auth_token)
    g = Github(auth=auth)
    return g

def myrepos() :
    repos=[]
    g = mygithub()
    for repo in g.get_user().get_repos():
        repos.append(repo.ssh_url)
    g.close()
    return(repos)

if __name__ == "__main__":

    local_prefix="/srv/git/mirrors/github/"
    g = mygithub()

    repolist_tmpname = tempfile.mktemp()
    print(repolist_tmpname)
    with open(repolist_tmpname,"w") as repolist:
        for repo in g.get_user().get_repos():
            url=repo.ssh_url
            shortname = url.split(':')[1].split('.')[0]
            local_copy=local_prefix+url.split(':')[1]

            repolist.write("repo.url="+url+"\n")
            repolist.write("repo.name="+shortname.split('/')[1]+"\n")
            # repolist.write("repo.url="+url+"\n")
            repolist.write("repo.owner=feurig\n")
            repolist.write("repo.path="+local_copy+"\n")
            description = repo.description
            if repo.description is None:
                description = "No Description Provided"
            repolist.write("repo.desc="+description+"\n")
            
            if os.path.isdir(local_copy):
                print("updating local copy: " + local_copy)
                result=subprocess.run(["git", "remote", "update"],
                                    cwd=local_copy, capture_output=True)
                print(result.stdout.decode(), end='')
                print(result.stderr.decode(), end='')            
            else:
                print("create new mirror at: "+local_copy)
                result=subprocess.run(["git","clone","--mirror", url, 
                                    local_copy], capture_output=True)
                print(result.stdout.decode(), end='')
                print(result.stderr.decode(), end='')
    g.close()
    
    os.replace(repolist_tmpname,"/srv/git/repolist")
    
