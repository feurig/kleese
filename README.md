# kleese

Git mirror Site and Code. (kleese is a git)

## TLDR:

- install pre-recs
- create git user with /srv/git as a home 
- su - git
- clone this repo
- create a github access token with read only access
- create /srv/git/kleese/.env file with AUTH_TOKEN="<the access token>"
- add */10 * * * * /srv/git/kleese/update_mirrors.py to git's crontab
- link etc/caddy/Caddyfile and etc/cgitrc into /etc/
- create and enable cgit.service
- enable caddy

## Goal (because apparently everything needs a fucking acceptance criteria)

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

PyGithup lets us get all of the repos that belong to me. The info we are interested in is in the [repository object](https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html)

#### Installing Pygithub on Debian

For some reason python3-github was different enough that I had to install PyGithub with pip and --break-system-packages.



So the idea is to check for all of the repos that I own/clone/participate in and mirror them. 

- foreach repo.
    - if repo is not mirrored
        - create a mirror
    - else 
        - update the mirror

### update_mirrors.py

The rudiments of a mirror program is at [https://github.com/feurig/kleese/blob/main/update_mirrors.py](https://github.com/feurig/kleese/blob/main/update_mirrors.py)

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

After extensive digging around I wanted to find a solution where I could mirror git repositories and access the mirrors using ssh. The only solution that did not require storing the repositories in a more complicated and proprietary way was cgit.As it turns out cgit and caddy are the simplest way to display the mirrored git repositories. unfortunately cgit is a cgi program. The easiest way to do cgi is fcgiwrap. Most of the tutorials use nginx which doesnt play well with unix sockets. After pulling my hair out, and perhaps realizing that the F5 branded nginx was being less than useful, [Footnote #1](#footnote_1)  I found a [1 page tutorial](https://www.sixfoisneuf.fr/posts/setting-up-cgit-with-caddy2/) that works.

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
git.suspectdevices.com {
    handle_path /cgit-css/* {
       root * /usr/share/cgit/
       file_server
    }
    handle {
            reverse_proxy localhost:8999 {
                        transport fastcgi {
                                env DOCUMENT_ROOT /usr/lib/cgit/
                                env SCRIPT_FILENAME /usr/lib/cgit/cgit.cgi
                                          }
                                         }
            }          
}
```

### configuring cgit

The /etc/gitrc below is rudimentry but it works. 

```sh
#
# cgit config
# see cgitrc(5) for details
css=/cgit-css/cgit.css
logo=/cgit-css/cgit.png
robots=nofollow

mimetype.html=text/html
mimetype.js=text/javascript
mimetype.css=text/css
mimetype.pl=text/x-script.perl
mimetype.pm=text/x-script.perl-module
mimetype.py=text/x-script.python
mimetype.png=image/png
mimetype.gif=image/gif
mimetype.jpg=image/jpeg
mimetype.jpeg=image/jpeg

root-title=SuspectDevices: Git 
root-desc=Mirror of public repositories

about-filter=/usr/lib/cgit/filters/about-formatting.sh
source-filter=/usr/lib/cgit/filters/syntax-highlighting.py

max-repo-count=100

readme=:README.md
readme=:README.txt
readme=:README.html
readme=:README

enable-git-config=1

#scan-path=/srv/git/mirrors/github/suspect-devices
#scan-path=/srv/git/mirrors/github
include=/srv/git/repolist
```
### Adding this file to the about section.

There is a root-readme directive which is supposed to add an about tab with the contents of the file referenced.

```sh
root-readme=/srv/git/kleese/README.md
```

Unfortunately cgit does not insure that the underlying python modules are installed to render it. 
Fortunatly this is easy enough to fix.

```sh
apt install -y python3-markdown
apt install -y python3-markdown-include
```

## Footnotes and References.

<a name="#footnote_1"> 1. </a> This is the second time recent nginx projects have foobarred unix sockets.

- https://www.sixfoisneuf.fr/posts/setting-up-cgit-with-caddy2/
- https://github.com/notzhan/blog/blob/main/post_source/setting-up-cgit-with-caddy.md
- https://pygithub.readthedocs.io/en/stable/github_objects/Repository.html
