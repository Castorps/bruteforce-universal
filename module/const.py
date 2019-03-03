

# Main Script
combos_max = 1000000  # maximum number of combos to load into memory
debug = False  # log each successful request (proxy ip + port + type, payload, response)

# Proxy Manager
proxies_minimum = 100  # if proxy list is smaller, scrape proxies
proxy_ban_time = 30  # time to wait after proxy ban to use it again
proxy_minimum_attempts = 3  # minimum attempts proxy has to do before calculating success ratio
proxy_success_ratio = 1/2  # = tested / retries, proxy gets deleted if value is smaller
proxy_timeout = 10  # time to wait before using proxy again

# Browser
auth_ssl = True
payload_json = False  # converts payload to json if true
payload_put = False  # if True: put, False: post
connection_timeout = 10
login_url = 'https://www.instagram.com/accounts/login/ajax/'  # used for authentication
home_url = 'https://www.instagram.com/'  # used to get cookies
headers = {}  # {<header_name>: <header_value>}; you may use {content_length}
headers_cookies = {'X-CSRFToken': 'csrftoken'}  # {<header_name>: <cookie_name>} (value will be cookie's value); empty? => won't look for cookies
payload = {'username': '{username}', 'password': '{password}'}  # {<field_name>: <field_value>}, use {username/password}
response_success = '"authenticated": true'  # if this is found in the response, authentication succeeded
response_error = 'generic_request_error'  # if this is found in the response, there was an error
