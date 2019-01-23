# Instagram Bruter:

Start an Instagram Bruteforce Attack using a combolist.

![Instagram-Bruter example](https://github.com/Castorps/Instagram-Bruter/blob/master/images/example.png)

You have to call [main.py](https://github.com/Castorps/Instagram-Bruter/blob/master/main.py) using two arguments:
  - `combo_file`: Path to the combolist you want to use.
  - `bots`: The number of bots to use.

On an ordinary Windows machine the starting command might look like this:

`python main.py "C:\user\myuser\combolist.txt" 250`

On Linux it might look like this:

`python ./main.py "/home/myuser/combolist" 250`


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


### Notes:
  - It shouldn't be too hard to use this tool for other websites, if you modify the [constants](https://github.com/Castorps/Instagram-Bruter/blob/master/module/const.py) and the [Browser](https://github.com/Castorps/Instagram-Bruter/blob/master/module/browser.py) appropriately.

  - There are other tools to generate combolists (see "combolist maker").
  
  - If you have stopped an attack, there is an output.txt in the same folder as your script, look at the Combolist Position and set the value of [`combos_start` in the constants](https://github.com/Castorps/Instagram-Bruter/blob/aebf33ea970156b6441c1eb321b839565d463116/module/const.py#L5) file to this. The next time you start an attack, the script will start from this position in the combolist. Remember to set `combos_start` to 0 again if you start an attack using a new combolist!
  
  - If you use your own proxies (you can put your own code into [Proxy Scraper's `scrape()` function](https://github.com/Castorps/Instagram-Bruter/blob/aebf33ea970156b6441c1eb321b839565d463116/module/proxy_scraper.py#L34), to read proxies from a file or to get them from other sources) and they require a username:password authentication, the proxy entries will have to look like this: `ip:port:type:username:password`; for example: `127.0.0.1:80:http:proxy_username:proxy_password` (`http` is the standard proxy type; supported types are `http`, `socks5`, `socks5h`)


##### ~~~ Inspired by [Pure-L0G1C's Instagram Bruteforce Tool](https://github.com/Pure-L0G1C/Instagram) ~~~

