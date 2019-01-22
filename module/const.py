

# Main Script
combos_max = 2000000  # maximum number of combos to load into memory
combos_start = 0  # combos from this point forward will be loaded into memory

# Proxy Manager
proxies_minimum = 250  # if proxy list is smaller, scrape proxies
proxy_ban_time = 30  # time to wait after proxy ban to use it again
proxy_minimum_attempts = 4  # minimum attempts proxy has to do before calculating success ratio
proxy_success_ratio = 1  # = tested / retries
proxy_timeout = 10  # time to wait before using proxy again

# Browser
auth_ssl = True
connection_timeout = 10
headers = {}  # {<header_name>: <header_value>}
headers_cookies = {'X-CSRFToken': 'csrftoken'}  # {<header_name>: <cookie_name>} (value will be cookie's value)
home_url = 'https://www.instagram.com/'  # used to get cookies
login_url = 'https://www.instagram.com/accounts/login/ajax/'  # used for authentication
payload = {'username': '{username}', 'password': '{password}'}  # {<field_name>: <field_value>}, use {username/password}
response_success = '"authenticated": true'  # if this is found in the response, authentication succeeded
response_error = 'error'  # if this is found in the response, there was an error
