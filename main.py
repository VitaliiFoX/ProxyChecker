import random
import requests
import os
from time import sleep
from proxychecker.constants import *


def check_proxy(proxy_id, current_proxy):             # Proxy must be proxy_type://login:pass@ip:port
    proxies = {
        'http': f'{current_proxy}',         # Recommended proxy type for socks5 is socks5h
        'https': f'{current_proxy}'
    }

    data = requests.get('https://whoer.net/en/main/api/ip', proxies=proxies).json()['data']
    ip = data['ip']

    request_params = {
        'key': IP2_LOCATION_API,
        'ip': ip
    }
    ip2location_data = requests.get('https://api.ip2location.io', proxies=proxies, params=request_params).json()
    proxy_geo = f"{data['iso']}_{ip2location_data['country_code']}"
    print(f"Checked {proxy_id + 1}/{total_proxies} proxy... The status of {proxy} is {proxy_geo}")
    return proxy_geo


def add_to_proxies(key, value):
    if key not in proxies_by_geo:
        proxies_by_geo[key] = [value]
    else:
        proxies_by_geo[key].append(value)


if __name__ == '__main__':
    with open(INPUT_FILE, 'r') as file:
        input_proxies = [line.rstrip() for line in file]

    total_proxies = len(input_proxies)
    print(f"There are {total_proxies} proxies")

    proxies_by_geo = {}
    for i, proxy in enumerate(input_proxies):
        try:
            geo = check_proxy(i, proxy)
            add_to_proxies(geo, proxy)
        except Exception as error:
            print(f"Error with proxy {proxy}: {error}. Added it to bad")
            add_to_proxies('BAD', proxy)

    if not os.path.exists(PATH_TO_RESULTS):
        os.mkdir(PATH_TO_RESULTS)

    for geo in proxies_by_geo:
        with open(os.path.join(PATH_TO_RESULTS, geo), 'w') as file:
            for proxy in proxies_by_geo[geo]:
                file.write(proxy + '\n')

