import os
import queue
import requests as req
from queue import Queue
from threading import Thread
from requests import Response

verified_file_path: str = './Proxies/verified-proxy.txt'

try:
    os.remove(path=verified_file_path)
except FileNotFoundError:
    print(f'File {verified_file_path} is not found.')

num_of_unverified_proxy: int = 0

# The queue the unverified proxies will occupy
proxy_queue: Queue[str] = queue.Queue()

# List of working proxies
valid_proxies: list[str] = []

with open(file='./Proxies/unverified-proxy.txt', mode='r') as f:
    proxies: list[str] = f.read().split(sep='\n')
    num_of_unverified_proxy = len(proxies)
    for proxy in proxies:
        proxy_queue.put(item=proxy)
    f.close()

def check_proxies() -> None:
    global proxy_queue
    while not proxy_queue.empty():
        proxy: str = proxy_queue.get()
        
        try:
            res: Response = req.get(
                url='http://ipinfo.io/json', 
                proxies={
                    'http': proxy, 
                    'https': proxy
                }
            )
            
            if res.status_code == 200:
                with open(file=verified_file_path, mode='a') as f:
                    f.write(f'{proxy}\n')
                    f.close()
        except:
            print(f'{proxy} not working!!! :(')
            continue

for _ in range(num_of_unverified_proxy - 1):
    Thread(target=check_proxies).start()