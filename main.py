import getToken
import requests
import base64
import re
import os

'''
通用文字识别
'''


# 判断是否有多选
def isMultipie(word):
    if re.search(r'\(可多选|多选题\)', word) != None:
        # 格式化可多选
        charIndex = word.find("(可多选)")
        if charIndex == -1:
            charIndex = word.find("(多选题)")
        word = word[0: charIndex - 1] + "[多选题]"
    else:
        word = ""
    return word


print("实例：C:\\\\Users\\\\dyedd\\\\Desktop\\\\test")
dir = input("批量识别的文件夹地址是：")
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
pic = os.listdir(r'{}'.format(dir))
# print(pic)

access_token = getToken.exeCute()

request_url = request_url + "?access_token=" + access_token

headers = {'content-type': 'application/x-www-form-urlencoded'}
i = 1
isFirst = ""
for picItem in pic:
    # 二进制方式打开图片文件
    f = open("{0}\\{1}".format(dir, picItem), 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        # print (response.json())
        # resultNum = response.json()['words_result_num']
        # print(resultNum)
        resultList = response.json()['words_result']
        for item in resultList:
            # print(item)
            # print(item['words'])
            word = item['words']
            # 去除识别的方框
            if "□" in word or "○" in word:
                word = word.lstrip("□")
                word = word.lstrip("○")
                isFirst = word
            elif re.match(r'\*\d|Q\d|\d+[.]*?[\u4e00-\u9fa5]+[^-].*', word) != None:
                # print(word)
                dotIndex = word.find(".")
                qmarkIndex = word.find("?")
                stopIndex = word.find("。")
                if qmarkIndex != -1:
                    # 结尾是问号
                    word2 = "{0}.{1}".format(i, word[dotIndex + 1:qmarkIndex + 1])
                    word = word2 + isMultipie(word)
                elif stopIndex != -1:
                    # 结尾是句号
                    word2 = "{0}.{1}".format(i, word[dotIndex + 1:stopIndex + 1])
                    word = word2 + isMultipie(word)
                else:
                    # 结尾什么都没有
                    word = "{0}.{1}".format(i, word[dotIndex + 1:]) + isMultipie(word)
                i += 1
                if isFirst != "":
                    print("")
            print(word)
