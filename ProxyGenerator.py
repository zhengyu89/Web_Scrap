import requests
import random
from bs4 import BeautifulSoup as bs
import traceback
import pandas as pd
import numpy as np

headers = {
    "User-Agent" :
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

def freeproxylist_generator(Limit = 50):
    url = "https://free-proxy-list.net/"

    resp = requests.get(url, headers=headers)
    df = pd.read_html(resp.content)[0]
    data = df[["IP Address","Port"]]
    Result_proxies_list = []
    for i in range(Limit):
        Proxies = {
                'http': f"http://{data.loc[i,"IP Address"]}:{data.loc[i,"Port"]}",
                'https': f"http://{data.loc[i,"IP Address"]}:{data.loc[i,"Port"]}"
                }
        Result_proxies_list.append(Proxies)
    return Result_proxies_list

# return list of proxy dictionary from proxyscrape.com
def proxyscrape_generator (Limit = 50):
    api = f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'

    resp = requests.get(api)
    proxy_list = resp.content.strip().decode('utf-8').strip().split('\n')
    #set the limit to avoid too many proxy obtained.
    limited_proxy_list = proxy_list[:Limit]
    Cleaned_proxy_list = []
    for i in limited_proxy_list:
        cleaned_proxy = i.replace('\r', '') 
        Proxies = {
                'http': f"http://{cleaned_proxy}",
                'https': f"http://{cleaned_proxy}"
                }
        Cleaned_proxy_list.append(Proxies)

    return Cleaned_proxy_list

#get ProxyList to make test
def Proxy_test(ProxysList):
    Proxys = ProxysList
    # make sure the proxy can be used
    for index in range(len(Proxys)):
        print (f"Request Number : {index +1}")
        Proxies = Proxys[index]
        try:
            resp = requests.get("https://httpbin.org/ip",headers=headers,proxies=Proxies)
            print(resp.content)
            break
        except TypeError:
            print("TypeError")
        except:
            print("Not available")

# Proxy_test(proxyscrape_generator(10))
# Proxy_test(freeproxylist_generator(10))
