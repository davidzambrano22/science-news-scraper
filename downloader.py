"""Science news info scraper """

import requests
import time

class Downloader:
    def __init__(self, user_agent = 'wswp', delay = 3, timeout = 60):
        self.user_agent = user_agent
        self.delay = delay
        #self.cache = cache
        self.timeout = timeout
    
    def __call__(self, url, num_retries):
        self.num_retries = num_retries
        try:
            result = self.cache[url]
            print('Loaded from cache', url)
        except KeyError:
            result = None
        
        if result and num_retries and 500 <= result['code'] < 600:
            result = None
        
        if result is None:
            headers = {'User-agent' : self.user_agent}
            result = self.Download(url, headers)
            self.cache[url] = result
            
        return result
    
    def Download(self, url):
        self.headers = {'User-agent' : 'wswp'}
        self.num_retries = 3
        print('Downloading: ', url)
        try:
            resp = requests.get(url = url, headers = self.headers, timeout= self.timeout)
            html = resp.text
            if 400 < resp.status_code:
                print('Download error:', resp.status_code)
                html = None
                if self.num_retries and 500 >= resp.status_code < 600:
                    #Recursive retry
                    self.num_retries -= 1
                    return self.Download(url)
        except requests.exceptions.RequestException as e :
            print('Download error: ', e)
            return {'html' : None, 'code' : 500}
        
        return {'html': html, 'code': resp.status_code}





