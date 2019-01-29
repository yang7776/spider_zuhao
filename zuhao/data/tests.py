from django.test import TestCase

# Create your tests here.

import urllib3
http = urllib3.PoolManager()
headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
url = 'https://www.zuhaowan.com/Appv2/Search/actRentDetailNew'
res = http.request('post',url,headers=headers,fields={'id':2014006})
print(res.data.decode())