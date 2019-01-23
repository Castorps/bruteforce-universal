

# Instagram Bruter:

![Version 1.7](https://img.shields.io/badge/Version-v1.7-blue.svg) ![Python 3.x.x](https://img.shields.io/badge/Python-v3.x.x-yellow.svg)

This script bruteforces Instagram accounts using a combolist. You have to provide the path to a combolist and how many bots you would like to use. To view found credentials, look at hits.txt in the script's directory.

![Instagram Bruter example](https://github.com/Castorps/Instagram-Bruter/blob/master/images/example.png)


### Features:
  - Cross-Platform
  - Multi-threaded (you can pick the number of bots)
  - Uses a combolist (attack multiple accounts at once)
  - Load combolist from a specified line (resume session)
  - Scrapes proxies automatically (also during the attack)
  - Deletes proxies that are failing too often automatically
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
  - requests
  - requests[socks]
 
 Install these using Python's pip:
 
    python -m pip install asciimatics

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

To add a proxy type (supported types: `http`, `socks5`, `socks5h`) append a colon and a type: `ip:port:type`

If a proxy requires username:password authentication, append the username and the password with a colon as separator: `ip:port:username:password`

A few examples:

    127.0.0.1:80
    
    127.0.0.1:6400:http
    
    127.0.0.1:6500:socks5
    
    127.0.0.1:6600:socks5h
    
    127.0.0.1:120:http:myname:secret_pass
    
    127.0.0.1:120:socks5:2nd_name:2nd_secret


### Notes: 
  - It shouldn't be too hard to use this tool for other websites, if you modify the [constants](https://github.com/Castorps/Instagram-Bruter/blob/master/module/const.py) and the [Browser](https://github.com/Castorps/Instagram-Bruter/blob/master/module/browser.py) appropriately.
  
  - If you have stopped an attack, there is an output.txt in the script's directory, look at the Combolist Position and set the value of [`combos_start` in the constants](https://github.com/Castorps/Instagram-Bruter/blob/aebf33ea970156b6441c1eb321b839565d463116/module/const.py#L5) file to this. The next time you start an attack, the script will start from this position in the combolist. Remember to set `combos_start` to 0 again if you start an attack using a new combolist!


#### ~~~ Inspired by [Pure-L0G1C's Instagram Bruteforce Tool](https://github.com/Pure-L0G1C/Instagram) ~~~
