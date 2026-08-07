#!/usr/bin/env python3




import os
import subprocess
from github import Github
from github import Auth
from dotenv import load_dotenv

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

#repo.url=wcm
#repo.owner=yctct
#repo.path=/home/git/repositories/wcm.git
#repo.desc= a script to count words in Markdown files
#
# Consider sorting by prefix and making group entries
if __name__ == "__main__":

    local_prefix="/srv/git/mirrors/github/"
    g = mygithub()
    with open("/srv/git/repolist", "w") as repolist:
        
        for repo in g.get_user().get_repos():
            url=repo.ssh_url
            shortname = url.split(':')[1].split('.')[0]
            local_copy=local_prefix+url.split(':')[1]

            repolist.write("repo.url="+shortname+"\n")
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
        
            #print(local_copy)
            #mypath="/srv/git/mirrors/github/"+repo.ssh_url.split(':')[1]
            #print("git clone --mirror " +repo.ssh_url+" "+mypath)
        g.close()
    