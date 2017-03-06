import functools
import json
import base64
from aiohttp import web
from aiohttp.web import Response
from spider import info_login, get_gender, get_name

api = web.Application()

def require_info_login(f):
    @functools.wraps(f)
    async def decorated_function(request, *args, **kwargs):
        # 获取POST的数据
        if request.method != 'POST':
            return Response(body = b'{}',
            content_type = 'application/json', status = 405)
        json_data = await request.json()
        sid = json_data.get('sid')
        pwd = json_data.get('pwd')
        s, sid, ip = await info_login(sid, pwd)
        if s is None:
            return Response(body = b'{}',
            content_type = 'application/json', status = 403)
            print('403')
        else:
            print('200')
            response = await f(request, s, sid, pwd, ip, *args, **kwargs)
            return response
    return decorated_function

@require_info_login
async def login_api(request, s, sid, pwd, ip):
    name = await get_name(sid)
    gender = await get_gender(sid, pwd, ip)
    if gender is None:
        gender = 0
    info = {'name': name, 'sno': sid}
    info['gender'] = gender
    return web.json_response(info)

api.router.add_route('*', '/login/', login_api, name='login_api')
