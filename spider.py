import random
import requests
import asyncio
import aioredis
import aiohttp
from bs4 import BeautifulSoup

info_login_url = "http://portal.ccnu.edu.cn/loginAction.do"
lib_login_url = "http://202.114.34.15/reader/redr_verify.php"
lib_me_url = "http://202.114.34.15/reader/redr_info.php"
console_api = "http://console.ccnu.edu.cn/ecard/getTrans?userId=%s&days=90&startNum=0&num=1"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:2.0b9pre) Gecko/20110105 Firefox/4.0b9pre'}

# async def redis_conn():
#     redis = await aioredis.create_redis(('localhost', 6379))
#     redis.slaveof(host='192.168.99.100', port=7389)
#     ips = await redis.smembers('ips')
#     redis.close()
#     await redis.wait_closed()
#     return ips

async def _info_login(session, payload, ip, sid, pwd):
    async with session.post(info_login_url, data=payload,
                            proxy=ip, timeout=4) as resp:
        resp_text = await resp.text()
        if resp_text.split('"')[1] == 'index_jg.jsp':
            _cookie_jar = session._cookie_jar
            return _cookie_jar, sid, ip
        else:
            return (None, sid, ip)

async def info_login(sid, pwd):
    _cookie_jar = None
    payload = {'userName': sid, 'userPass': pwd}
    # ips = await redis_conn() # 每次请求都会调用
    while True: # 错误重试
        # ip = random.choice(ips).decode()
        ip = None
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                s, sid, ip = await _info_login(session, payload, ip, sid, pwd)
                return (s, sid, ip)
            except Exception as e:
                pass

async def _lib_login(payload):
    # blocking... aiohttp 就是一个shit 不得不用requests
    s = requests.Session() 
    s.post(lib_login_url, payload, headers=headers)
    r = s.get(lib_me_url)
    if '123456'.encode() in r.content:
        return None
    else:
        return r.content

async def lib_login(sid, pwd):
    print(sid)
    payload = {'number': sid, 'passwd': '123456', 'select': 'cert_no'}
    # payload = aiohttp.FormData(payload)
    # async with aiohttp.ClientSession(headers=headers) as session:
    #     session._unsafe = True
    #     async with session.post(lib_login_url, data=payload):
    #         async with session.get(lib_me_url) as resp:
    #             resp_text = await resp.text()
    #             if '123456' in resp_text:
    #                 return None
    #             return resp_text
    rv = await _lib_login(payload)
    return rv
    
async def get_name(sid):
    async with aiohttp.ClientSession(headers=headers) as session:
        console_sid_api = console_api % sid
        async with session.get(console_sid_api) as resp:
            json_data = await resp.json()
            return json_data[0]['userName']

async def get_gender(sid, pwd):
    # 假装模拟登录图书馆, 获取性别
    resp_text = await lib_login(sid, pwd)
    if resp_text:
        # 获取性别
        soup = BeautifulSoup(resp_text, 'lxml')
        mylib_info = soup.find('div', id='mylib_info')     
        gender_info = mylib_info.find_all('tr')[-3].find_all('td')[-1].text
        if '男' in gender_info: return 1
        if '女' in gender_info: return 2
        return None
    else: return None
