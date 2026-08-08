# kleese

Git mirror Site and Code. (kleese is a git)

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

## The github mirror


### PyGithub

For some reason python3-github was different enough that I had to install PyGithub with pip and --break-system-packages.

https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html

So the idea is to check for all of the repos that I own/clone/participate in and mirror them. 

- foreach repo.
    - if repo is not mirrored
        - create a mirror
    - else 
        - update the mirror

### update_mirrors.py

The rudiments of a mirror program is at https://github.com/feurig/kleese/blob/main/update_mirrors.py

```sh
apt install -y python3-pip python3-pygit2 python3-dotenv cron
pip install PyGithub --break-system-packages
su -l git
git clone git@github.com:feurig/kleese.git
crontab -e 
... Add the following ...
*/10 * * * * /srv/git/kleese/update_mirrors.py
```

## cgit and caddy

After extensive digging around I wanted to find a solution where I could mirror git repositories and access the mirrors using ssh. The only solution that did not require storing the repositories in a more complicated and proprietary way was cgit.As it turns out cgit and caddy are the simplest way to display the mirrored git repositories. unfortunately cgit is a cgi program. The easiest way to do cgi is fcgiwrap. Most of the tutorials use nginx which doesnt play well with unix sockets. After pulling my hair out and perhaps realizing that the F5 branded nginx was being less than useful. [Footnote #1](#footnote_1) Fortunately I found a [1 page tutorial](https://www.sixfoisneuf.fr/posts/setting-up-cgit-with-caddy2/) that works.

First we install the software.

```sh
apt install -y caddy fcgiwrap cgit python3-pygments man
```

Rather than modify fcgiwrap's configuration create a new service.

```sh
systemctl edit --full --force cgit.service
... Add the following ...
[Unit]
Description=CGI web interface to the Git SCM
After=network.target

[Service]
Type=exec
ExecStart=fcgiwrap -f -p "/usr/lib/cgit/cgit.cgi" -s tcp:127.0.0.1:8999

[Install]
WantedBy=multi-user.target
...
systemctl start cgit
```
This is combined with the following caddy file serves up the cgit.

```sh

```

- https://www.sixfoisneuf.fr/posts/setting-up-cgit-with-caddy2/
- https://github.com/notzhan/blog/blob/main/post_source/setting-up-cgit-with-caddy.md
