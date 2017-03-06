# 武理 % 华师

> 3.7女生节活动华师登入接口

<hr/>

| URL |  Header | Method |
| ------------- |:-------------:| -----:|
| /api/login/ | 无特殊header | POST, GET |

<hr/>

## URL Params
无url 参数

## POST Data(json)

    {
        "sid": "学号",
        "pwd": "密码"
    }

## Return Data(json)

    {
        "name": "姓名",
        "sno": "学号",
        "gender" 1 # 男生->1, 女生->2, 无法获取性别->0
    }

## Status Code

+ 200 ok
+ 403 用户名或密码错误
+ 502 服务器端错误
