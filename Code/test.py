import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent


def Request_Header():
    """_summary_
    浏览器请求头伪装
        Returns:
            {}: 浏览器请求头
    """
    headers = {"User-Agent": UserAgent().random}

    return headers


headers = {"User-Agent": "XXXX"}
# 视频id
oid = 32612698
# 评论页数
pn = 1
# 排序种类 0是按时间排序 2是按热度排序
sort = 2

while True:
    url = f"https://api.bilibili.com/x/v2/reply?pn={pn}&type=12&oid={oid}&sort={sort}"
    reponse = requests.get(url, headers=headers)
    a = json.loads(reponse.text)
    print(a)
    if pn == 1:
        count = a["data"]["page"]["count"]
        size = a["data"]["page"]["size"]
        page = count // size + 1
        print(page)
    for b in a["data"]["replies"]:
        # print(b["content"]["message"])
        print("-" * 10)
    if pn != page:
        pn += 1
    else:
        break
