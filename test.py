#!/usr/bin/env python3

import os
from github import Github
from github import Auth
from dotenv import load_dotenv

load_dotenv()
    
auth_token = os.environ["AUTH_TOKEN"]

def mygithub() :
    auth = Auth.Token(auth_token)
    g = Github(auth=auth)
    return g


if __name__ == "__main__":
    g = mygithub()
    for repo in g.get_user().get_repos():
        #print(repo.name)
        mypath="/srv/git/mirrors/github/"+repo.ssh_url.split(':')[1]
        print("git clone --mirror " +repo.ssh_url+" "+mypath)
        
    g.close()
