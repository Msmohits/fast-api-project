import json

import requests
from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from requests import request
import webbrowser
import uvicorn
import urllib
from urllib.parse import urlparse, parse_qs


app = FastAPI()


@app.get('/')
async def vryno_token():
    auth_url = 'https://test2acc.vryno.dev/oidc/auth?response_type=code&client_id=7udyDbn9gD7peBEzubWMxx&client_secret=TWCGlWXYzfNJllplxyKmrc1hVcm9Un2qroCZj9H2fA4&scope=openid%20vryno_offline_access&redirect_uri=https%3A%2F%2Fgateway.ddns.net%2Fmy_data&code_challenge=4UfI52WlX7QpCc7GPD7akeI2VpziEQ0V2_N1WU-uMXY&code_challenge_method=S256'
    # auth_url = 'https://test2acc.vryno.dev/oidc/auth?response_type=code&client_id=7FtfW19eUeWemkZ9m3Qm7u&scope=openid%20vryno_offline_access&redirect_uri=http%3A%2F%2Flapp.vryno.dev%3A8001%2Fget_code&code_challenge=WpqT5mGv9VEtv7UKdm3kY4IKqq4xHYE-rpdv-iZumTg&code_challenge_method=S256'
    # auth_url = '''https://test2acc.vryno.dev/oidc/auth?response_type=code&code_challenge_method=S256&code_challenge=HG89Ycj4BC0XTnVfVFCYAdWUHKVtdWFyHTVZ3FfMV3k&client_id=WS7qF93G48j8R3aYtoEXbj&client_secret=8aefXbx4OEka4UFLMv6ZyEtqWS6f98fzXzmeq1iz4ia&scope=openid vryno_offline_access&redirect_uri=http://lapp.vryno.dev:8001/get_code'''
    webbrowser.open(auth_url, new=False)
    # resposne = requests.get(auth_url)
    # print(resposne)

# todo this api is implemented on a different server with restapi here am getting the code but but response_type<400>
@app.route('/my_data', methods=['GET'])
def my_data():
    data = request.args

    code = data.get('code')
    iss = data.get('iss')
    print('args', data, code)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Host": "test2acc.vryno.dev",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Content-Length": "285"
    }

    body = {
        "grant_type": "authorization_code",
        "code": str(code),
        "redirect_uri": "http://lapp.vryno.dev:8001/get_code",
        "client_id": "7udyDbn9gD7peBEzubWMxx",
        "client_secret": "TWCGlWXYzfNJllplxyKmrc1hVcm9Un2qroCZj9H2fA4",
        "scope": "openid vryno_offline_access"
    }
    print(body)

    url = "https://test2acc.vryno.dev/oidc/token"
    response_type = requests.post(url, headers=headers, data=body)
    print(response_type, )
    return 'success'


@app.get('/get_code')
def get_code(request: Request):

    print('ssssss',request.json)
    return 'success'


if __name__ == '__main__':
    uvicorn.run("test3:app", port=8001, host="0.0.0.0")
