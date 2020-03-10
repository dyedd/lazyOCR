import requests


def exeCute():
    print("===禁止白嫖怪，所以... ===")
    print("")
    ak = input("输入您得到的API Key：")
    sk = input("输入您得到的Secret Key：")
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={ak}&client_secret={sk}'.format(
        ak=ak, sk=sk)
    response = requests.get(host)
    if response:
        if "access_token" in response.json():
            token = response.json()["access_token"]
            return token
        else:
            # print(response.json())
            return response.json()
