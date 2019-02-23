

# Main Script
combos_max = 1000000  # maximum number of combos to load into memory
debug = True  # log each successful request (proxy ip + port + type, payload, response)

# Proxy Manager
proxies_minimum = 40  # if proxy list is smaller or equal, scrape proxies
proxy_ban_time = 30  # time to wait after proxy ban to use it again
proxy_minimum_attempts = 3  # minimum attempts proxy has to do before calculating success ratio
proxy_success_ratio = 1/2  # = tested / retries, proxy gets deleted if value is smaller
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
response_error = 'generic_request_error'  # if this is found in the response, there was an error
