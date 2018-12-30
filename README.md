# Instagram Bruter:

Start a Instagram Bruteforce Attack using a proxylist and comblist.

You have to call [main.py](https://github.com/EagerToLearn34/InstagramBruter/blob/master/main.py) using three arguments ('*combo_file*', '*proxy_file*', '*hits_file*', '*bots*').
  - *combo_file*: Path to the combolist you want to use.
  - *proxy_file*: Path to the proxylist you want to use (the script does not scrape new proxies for you!).
  - *hits_file*: Path to a file you want to store working credentials in (the script will create this file).
  - *bots*: The number of bots to use.
  
example:

`python main.py "C:\my user\combolist.txt" "C:\my user\proxylist.txt" "C:\my user\hits.txt" 250`
 
If you want to change other variables (like the time a proxy is disabled after it has been used and the connection timeout), take a look at the [constant file](https://github.com/EagerToLearn34/InstagramBruter/blob/master/lib/const.py).


### Requirements:
  - requests
  - asciimatics
 
 Install these using *pip*:
 
  `python -m pip install requirements`
 
  `python -m pip install asciimatics`
 

### Notes:
  - The combolist is a text file, each lines contains a username and a password, like this: [username]:[password]
  - The proxylist is a text file, each line contains an IP address and a port, like this: [ip]:[port]
  - It shouldn't be too hard to use this tool for other websites if you modify const.py and browser.py appropriately.


### Workflow:
  1. Load combolist into memory.
  
  2. Start the [Proxy Scraper](https://github.com/EagerToLearn34/InstagramBruter/blob/master/lib/proxy_scraper.py), which loads proxies from the proxylist into memory. It will automatically load proxies again if a limit is undershot.
  
  2. Start the [Proxy Manager](https://github.com/EagerToLearn34/InstagramBruter/blob/master/lib/proxy_manager.py), which takes care of managing proxies (see below). 
  
  3. Start [Bruter](https://github.com/EagerToLearn34/InstagramBruter/blob/master/lib/bruter.py), which starts Bots, these are workers that each take a username-password combination and a proxy and try to authenticate using the [Browser](https://github.com/EagerToLearn34/InstagramBruter/blob/master/lib/browser.py). After being used, each proxy gets disabled for some seconds, which means that it can't be used for authentication attempts.
  
  4. The script keeps track of the number of authentication attemps, tested credentials, attempts per minute on average, tests per minute on average, tests of each proxy and retries of each proxy.
  
  5. The Proxy Manager will remove proxies that don't have a sufficient success ratio (tested credentials divided by retries) and it will enable proxies that have been disabled if enough time has passed.
  
Any improvements, ideas, suggestions are welcome!


##### ~~~ Inspired by [Pure-L0G1C's Instagram Bruteforce Tool](https://github.com/Pure-L0G1C/Instagram) ~~~

