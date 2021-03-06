

# Bruteforce Tool:

![Version 2.1](https://img.shields.io/badge/Version-v2.1-blue.svg) ![Python 3.x.x](https://img.shields.io/badge/Python-v3.x.x-yellow.svg)

This script bruteforces accounts using a combolist. You have to provide the path to a combolist and how many bots you would like to use. To view found credentials, look at hits.txt in the script's directory.

![Instagram Bruter example](https://github.com/Castorps/Instagram-Bruter/blob/master/images/example_attack.png)


### Features:
  - Cross-Platform
  - Multi-threaded (you can pick the number of bots)
  - Uses a combolist (attack multiple accounts at once)
  - Saves and resumes sessions
  - Scrapes proxies automatically (40k+ unique proxies; also during the attack)
  - Deletes proxies that are producing too many errors automatically
  - Rotates proxies to avoid blocking


### Usage:
You have to start [bruteforce.py](https://github.com/Castorps/Instagram-Bruter/blob/master/bruteforce.py) with two parameters:
  - `combo_file`: The path to the combolist you want to use.
  - `bots`: The number of bots to use.

Like this:

    python bruteforce.py "<combo_file>" <bots>


### Requirements:
  - Python 3.x.x


### Dependencies:
  - asciimatics
  - bs4
  - requests
  - requests[socks]
 
 Install these using Python's pip:
 
    python -m pip install asciimatics
    
    python -m pip install bs4

    python -m pip install requests

    python -m pip install requests[socks]


### Configuration: Combolist
The combolist is a text file, each line contains a username and a password in `username:password` format. There are many tools to generate combolists out there (see "combolist maker").

A few examples:

    myusername:mypassword

    daniel:abc123

    daniel:isthismypassword

    alex:987654321


#### Advanced Configuration: Constants
If you want to change other variables (like the connection timeout and how long to wait before reusing a proxy), take a look at the [constant file](https://github.com/Castorps/Instagram-Bruter/blob/master/module/const.py).


#### Advanced Configuration: Personal Proxies / Proxy Type / Proxy Authentication
If you want to use your own proxies you have to harvest them using [Proxy Scraper's `scrape()` function](https://github.com/Castorps/Instagram-Bruter/blob/aebf33ea970156b6441c1eb321b839565d463116/module/proxy_scraper.py#L34). The proxies have to be passed on in `ip:port` format.

To add a proxy type (default is `http`; supported types: `http`, `socks5`, `socks5h`) append a colon and a type: `ip:port:type`

If a proxy requires username:password authentication, append the username and the password with a colon as separator: `ip:port:type:username:password`

A few examples:

    127.0.0.1:80
    
    127.0.0.1:6400:http
    
    127.0.0.1:6500:socks5
    
    127.0.0.1:6600:socks5h
    
    127.0.0.1:120:http:myname:secret_pass
    
    127.0.0.1:120:socks5:2nd_name:2nd_secret


### Notes: 
  - The default setup is configured for Instagram, but if you modify the [constants](https://github.com/Castorps/Instagram-Bruter/blob/master/module/const.py) and the [Browser](https://github.com/Castorps/Instagram-Bruter/blob/master/module/browser.py) appropriately, you can use this tool for other websites.


#### ~~~ Inspired by [Pure-L0G1C's Instagram Bruteforce Tool](https://github.com/Pure-L0G1C/Instagram) ~~~
