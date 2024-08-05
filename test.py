import os
import json
import queue
import requests as req
from queue import Queue
from io import TextIOWrapper
from threading import Thread
from requests import Response

# Get the constants from the json file
constants: TextIOWrapper = open(file='./constants.json')

# Takes a json data and returns a dictionary
constants_dict: dict[str, str] = json.load(fp=constants)

# Constants
verified_file_path: str = constants_dict.get('verified_file_path') # type: ignore
unverified_file_path: str = constants_dict.get('unverified_file_path') # type: ignore
ip_testing_url: str = constants_dict.get('ip_testing_url') # type: ignore

# Delete the verified_file.txt if it exists
def delete_verified_proxy_file(file_path: str) -> None:
    try:
        os.remove(path=file_path)
    except FileNotFoundError:
        print(f'File {file_path} is not found.\n')

# Get all the proxies from unverified_proxy.txt
def get_proxies(file_path: str) -> Queue[str]:
    # The queue the unverified proxies will occupy
    proxy_queue: Queue[str] = queue.Queue()
    
    with open(file=file_path, mode='r') as f:
        proxies: list[str] = f.read().split(sep='\n')
        for proxy in proxies:
            proxy_queue.put(item=proxy)
        f.close()
    
    return proxy_queue

def check_proxies() -> None:
    global proxy_queue
    while not proxy_queue.empty():
        proxy: str = proxy_queue.get()
        
        try:
            res: Response = req.get(
                url=ip_testing_url, 
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
        

if __name__ == '__main__':
    delete_verified_proxy_file(file_path=verified_file_path)
    
    proxy_queue: Queue[str] = get_proxies(file_path=unverified_file_path)
    
    queue_length: int = proxy_queue.qsize() - 1
    
    for _ in range(queue_length):
        Thread(target=check_proxies).start()