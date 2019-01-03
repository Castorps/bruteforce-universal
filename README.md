# Instagram Bruter:

Start an Instagram Bruteforce Attack using a proxylist and a combolist.

You have to call [main.py](https://github.com/Castorps/Instagram-Bruter/blob/master/main.py) using four arguments:
  - `combo_file`: Path to the combolist you want to use.
  - `proxy_file`: Path to the proxylist you want to use (the script loads proxies, but does not scrape them you!).
  - `hits_file`: Path to a file you want to store working credentials in (the script will create this file).
  - `bots`: The number of bots to use.
  
On an ordinary Windows machine the starting command might look like this:

`python main.py "C:\my user\combolist.txt" "C:\my user\proxylist.txt" "C:\my user\hits.txt" 250`

 
If you want to change other variables (like the connection timeout and how often a proxy may be used for authentication attempts during a certain time span), take a look at the [constant file](https://github.com/Castorps/Instagram-Bruter/blob/master/module/const.py).


### Requirements:
  - asciimatics
  - requests
 
 Install these using Python's pip:
 
   `python -m pip install asciimatics`

   `python -m pip install requirements`
 

### Notes:
  - The combolist is a text file, each lines contains a username and a password: 
  
    `myusername:mypassword`

    `daniel:abc123`

    `daniel:isthismypassword`

    `alex:987654321`
  
  
  - The proxylist is a text file, each line contains at least an IP address and a port:
  
    `127.0.0.1:80`

    `127.0.0.1:23000`
  
  
  - Each line in the proxylist (thus each proxy) may contain additional information about the proxy, like the type of the proxy (supported types: `http`, `socks5`, `socks5h`) as well as a username and a password for the proxy. These may be appended to each line with a `:` as separator. If you omit these parameters, the default proxy type `http` and no username and no password for the proxy will be used. A few examples:
  
    `127.0.0.1:80`
  
    `127.0.0.1:1200:socks5`
  
    `127.0.0.1:25420:socks5:my_proxy_username:my_proxy_password`
    
  
  - It shouldn't be too hard to use this tool for other websites, if you modify the [constants](https://github.com/Castorps/Instagram-Bruter/blob/master/module/const.py) and the [Browser](https://github.com/Castorps/Instagram-Bruter/blob/master/module/browser.py) appropriately.
  
  - There are other tools to generate combolists (see "combomaker") and proxylists (see "proxy scraper"). You may include code to scrape proxies in [proxy_scraper.py's `scrape()` function](https://github.com/Castorps/Instagram-Bruter/blob/d07c8c047bcbe12345f0236f700a96983d5e010f/module/proxy_scraper.py#L9).


### Workflow:
  1. Load combolist into memory.
  
  2. Start the [Proxy Scraper](https://github.com/Castorps/Instagram-Bruter/blob/master/module/proxy_scraper.py), which loads proxies from the proxylist into memory. It will automatically load proxies from the proxylist if a limit is undershot.
  
  2. Start the [Proxy Manager](https://github.com/Castorps/Instagram-Bruter/blob/master/module/proxy_manager.py), which takes care of managing proxies (see below). 
  
  3. Start [Bruter](https://github.com/Castorps/Instagram-Bruter/blob/master/module/bruter.py), which starts Bots, these are workers that each take a username-password combination and a proxy and try to authenticate using the [Browser](https://github.com/Castorps/Instagram-Bruter/blob/master/module/browser.py). After being used, each proxy gets disabled for a few seconds, during this period of time, it may not be used for authentication attempts.
  
  4. The script keeps track of the number of authentication attemps, tested credentials, attempts per minute on average, tests per minute on average, tests of each proxy and retries of each proxy.
  
  5. The [Proxy Manager](https://github.com/Castorps/Instagram-Bruter/blob/master/module/proxy_manager.py) will remove proxies that don't have a sufficient success ratio (tested credentials divided by retries) and it will enable proxies that have been disabled once a certain waiting time has passed.
  
Any improvements, ideas, suggestions are welcome!


##### ~~~ Inspired by [Pure-L0G1C's Instagram Bruteforce Tool](https://github.com/Pure-L0G1C/Instagram) ~~~

