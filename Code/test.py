import pickle
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


def get_cookies():
    with open("Data\登录文件\cookies文件.pickle", "rb") as file:
        cookiesList = pickle.load(file)
    return cookiesList


def Get_Comment():
    cookies_dict = {cookie["name"]: cookie["value"] for cookie in get_cookies()}
    # 专栏id
    oid = 32447224
    # 评论页数
    pn = 1
    # 排序种类 0是按时间排序 2是按热度排序
    sort = 2
    while True:
        url = (
            f"https://api.bilibili.com/x/v2/reply?pn={pn}&type=12&oid={oid}&sort={sort}"
        )
        reponse = requests.get(url, headers=Request_Header(), cookies=cookies_dict)
        a = json.loads(reponse.text)
        print(a)
        if pn == 1:
            count = a["data"]["page"]["count"]
            size = a["data"]["page"]["size"]
            page = count // size + 1
        for b in a["data"]["replies"]:
            print(b["content"]["message"])
            print("-" * 10)
        if pn != page:
            pn += 1
        else:
            break
