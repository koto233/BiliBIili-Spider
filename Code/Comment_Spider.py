import os
from random import choice
import random
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv


# 浏览器请求头伪装
def request_header():
    headers = {"User-Agent": UserAgent().random}
    return headers


def Get_Url(cid, page, sort):
    """_summary_
    地址规则 https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=[]&type=17&oid=[]&sort=[]
    cid为专栏种类
    cid=2 : 动画
    cid=1 : 游戏
    cid=28 : 影视
    cid=3 : 生活
    cid=29 : 兴趣
    cid=16 : 轻小说
    cid=17 : 科技
    cid=41 : 笔记
    sort为排序方式
    sort=1 : 投稿时间排序
    sort=2 : 点赞数最多
    sort=3 : 评论数最多
    sort=4 : 收藏数最多
    参数:
        cid (int) : 专栏种类
        page(int) : 页数
        sort(int) : 排序
    Returns:
        string: 网址
    """
    url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=[]&type=17&oid=[]&sort=[]"
    return url


# 开爬
def Get_Comment():
    cookies_string = "buvid3=62767AD5-95A0-2DF3-7B9E-9654C3B4892E44478infoc; b_nut=1696593043; _uuid=9DB65102B-1854-9B510-7BF10-743A1052A6B7B46728infoc; hit-dyn-v2=1; buvid_fp_plain=undefined; rpdid=0zbfVHggsG|K4P8OKjM|3cZ|3w1QOKb1; balh_server_inner=__custom__; balh_is_closed=; buvid4=64A21B2F-BB6F-0D4A-C8D3-398E9816747644478-023100619-GlJ98KWPjQp%2Fiw4HFg%2B03Q%3D%3D; LIVE_BUVID=AUTO9016965992146911; CURRENT_BLACKGAP=0; ogv_channel_version=v1; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_QUALITY=80; is-2022-channel=1; DedeUserID=11991721; DedeUserID__ckMd5=98268ae3f3eecc9f; fingerprint=0116960deda650739eb876fc011d5f37; FEED_LIVE_VERSION=V_FAVOR_WATCH_LATER; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDk2MzU3MzIsImlhdCI6MTcwOTM3NjQ3MiwicGx0IjotMX0.9T2dA8HAj3uiMET8a4sODnj0HUQWCkTdNUT0P7ZKFN4; bili_ticket_expires=1709635672; SESSDATA=dece522c%2C1724938794%2C50453%2A31CjBFsmtlw0X_JmNpLQ1WXsPfaVu4XSQ3tz_U7QLGF1zSiW9I-nGBRWyMzkHV5-fOpu4SVjJWZUFkUWZYQ0lEQ0Y0SnlrekNUS09kekI2aXpYTF9FbWZDMm0tbVc0Ym12ZWN5ajFRY3huZXJNRjFkb2dEVndSTUhsLWRBc19xdi1FUy1GVnpibDFRIIEC; bili_jct=c50413b08d38cb7dc2f40ca8ce5b2957; buvid_fp=0116960deda650739eb876fc011d5f37; b_lsid=BBADA3C10_18E03861A47; bp_video_offset_11991721=904589656688951313; home_feed_column=4; browser_resolution=502-809; bsource=search_bing"
    cookies = dict([cookie.split("=") for cookie in cookies_string.split("; ")])
    # cidName_li = ["动画", "游戏", "影视", "生活", "兴趣", "轻小说", "科技", "笔记"]
    cidName_li = ["动画"]
    id_url_dict = {}
    for i in range(len(cidName_li)):
        csv_file = f"Data\{cidName_li[i]}.csv"
        print(csv_file)
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            # 跳过标题行（如果存在）
            next(reader, None)  # 这会读取第一行（即标题行）并跳过它
            # 逐行读取CSV文件
            for row in reader:
                if row:  # 确保行不为空
                    # 假设第一列是ID，最后一列是View URL
                    id = row[0]
                    view_url = row[-1]
                    id_url_dict[id] = view_url
        # 打印字典内容来验证
        for id, url in id_url_dict.items():
            print(f"开始爬取ID为{id}的文章, 地址：{url}")
            folder_name = f"Data/{cidName_li[i]}_评论"
            file_name = f"{folder_name}/{id}_comments.txt"
            # 使用os.makedirs创建目录，exist_ok=True表示如果目录已经存在不会抛出异常
            os.makedirs(folder_name, exist_ok=True)


if __name__ == "__main__":
    Get_Comment()
