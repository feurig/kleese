# kleese
Git mirror code (kleese is a git)

## Goal.
With microsoft and atlassian enshittifying everything mirror your content to servers you control. 

### start with github 

Github contains our public repositories.

- write enough python to automate mirrors to git.suspectdevices.com
- install cgit and evaluate it for an easy view of the codes. 
- keep the source of truth on github mirror until it doesn't make sense to. 
- consider moving the blog content to git.suspectdevices.com just to be courteous.

### Move on to bitbucket. 
Bitbucket is where our private repositories are kept. 
- write enough python to automate mirrors to (katherine aka mia zapatta of the Gits.) git server at home.

## The Python

### PyGithub

For some reason python3-github was different enough that I had to install PyGithub with pip and --break-system-packages.

https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html

So the idea is to check for all of the repos that I own/clon/participate in and mirror them. 

- foreach repo.
    - if repo is not mirrored
        - create a mirror
    - else 
        - update the mirror

## cgit

