# Instagram Bruter:

Start an Instagram Bruteforce Attack using a proxylist and a combolist.

![Instagram-Bruter example](https://github.com/Castorps/Instagram-Bruter/blob/master/images/example.png)

You have to call [main.py](https://github.com/Castorps/Instagram-Bruter/blob/master/main.py) using three arguments:
  - `combo_file`: Path to the combolist you want to use.
  - `proxy_file`: Path to the proxylist you want to use (the script loads proxies, but does not scrape them for you!).
  - `bots`: The number of bots to use.
  
On an ordinary Windows machine the starting command might look like this:

`python main.py "C:\my user\combolist.txt" "C:\user\myuser\proxylist.txt" 250`

On Linux it might look like this:

`python main.py "/home/user/combolist" "/home/myuser/proxylist" 250`

 
If you want to change other variables (like the connection timeout, where to pickup the attack after restarting the script and how often a proxy may be used for authentication attempts during a certain time span), take a look at the [constant file](https://github.com/Castorps/Instagram-Bruter/blob/master/module/const.py).


### Requirements:
  - asciimatics
  - requests
  - requests[socks]
 
 Install these using Python's pip:
 
  `python -m pip install asciimatics`

  `python -m pip install requests`
   
  `python -m pip install requests[socks]`
 

### Combolist:
  - The combolist is a text file, each lines contains a username and a password: 
  
    `myusername:mypassword`

    `daniel:abc123`

    `daniel:isthismypassword`

    `alex:987654321`
  
### Proxylist:  
  - The proxylist is a text file, each line contains at least an IP address and a port:
  
    `127.0.0.1:80`

    `127.0.0.1:23000`
  
  
  - Each line in the proxylist (thus each proxy) may contain additional information about the proxy, like the type of the proxy (supported types: `http`, `socks5`, `socks5h`) as well as a username and a password for the proxy. These may be appended to each line with a `:` as separator. If you omit these parameters, the default proxy type `http` and no username and no password for the proxy will be used. A few examples:
  
    `127.0.0.1:80`
  
    `127.0.0.1:1200:socks5`
  
    `127.0.0.1:25420:socks5:my_proxy_username:my_proxy_password`
    
  
### Notes:
  - It shouldn't be too hard to use this tool for other websites, if you modify the [constants](https://github.com/Castorps/Instagram-Bruter/blob/master/module/const.py) and the [Browser](https://github.com/Castorps/Instagram-Bruter/blob/master/module/browser.py) appropriately.
  
  - There are other tools to generate combolists (see "combolist maker") and proxylists (see "proxy scraper"). You may include code to scrape proxies in [proxy_scraper.py's `scrape()` function](https://github.com/Castorps/Instagram-Bruter/blob/d07c8c047bcbe12345f0236f700a96983d5e010f/module/proxy_scraper.py#L9).


##### ~~~ Inspired by [Pure-L0G1C's Instagram Bruteforce Tool](https://github.com/Pure-L0G1C/Instagram) ~~~

