import csv
import requests
import time
import pandas as pd
import json
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from browsermobproxy import Server
from selenium.webdriver.common.keys import Keys
import re
from selenium import webdriver
from seleniumwire import webdriver as swd
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent


# 浏览器请求头伪装
def request_header():
    headers = {"User-Agent": UserAgent().random}
    return headers


# 调用函数scroll将左侧的滚动条滑动到底部
def scroll(driver):
    driver.execute_script(
        """ 
        (function () { 
            var y = document.body.scrollTop; 
            var step = 100; 
            window.scroll(0, y); 
            function f() { 
                if (y < document.body.scrollHeight) { 
                    y += step; 
                    window.scroll(0, y); 
                    setTimeout(f, 50); 
                }
                else { 
                    window.scroll(0, y); 
                    document.title += "scroll-done"; 
                } 
            } 
            setTimeout(f, 1000); 
        })(); 
        """
    )


def get_cookies():
    cookies_str = "buvid3=62767AD5-95A0-2DF3-7B9E-9654C3B4892E44478infoc; b_nut=1696593043; _uuid=9DB65102B-1854-9B510-7BF10-743A1052A6B7B46728infoc; hit-dyn-v2=1; buvid_fp_plain=undefined; rpdid=0zbfVHggsG|K4P8OKjM|3cZ|3w1QOKb1; balh_server_inner=__custom__; balh_is_closed=; buvid4=64A21B2F-BB6F-0D4A-C8D3-398E9816747644478-023100619-GlJ98KWPjQp%2Fiw4HFg%2B03Q%3D%3D; LIVE_BUVID=AUTO9016965992146911; CURRENT_BLACKGAP=0; ogv_channel_version=v1; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_QUALITY=80; is-2022-channel=1; DedeUserID=11991721; DedeUserID__ckMd5=98268ae3f3eecc9f; fingerprint=0116960deda650739eb876fc011d5f37; FEED_LIVE_VERSION=V_FAVOR_WATCH_LATER; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDk2MzU3MzIsImlhdCI6MTcwOTM3NjQ3MiwicGx0IjotMX0.9T2dA8HAj3uiMET8a4sODnj0HUQWCkTdNUT0P7ZKFN4; bili_ticket_expires=1709635672; SESSDATA=dece522c%2C1724938794%2C50453%2A31CjBFsmtlw0X_JmNpLQ1WXsPfaVu4XSQ3tz_U7QLGF1zSiW9I-nGBRWyMzkHV5-fOpu4SVjJWZUFkUWZYQ0lEQ0Y0SnlrekNUS09kekI2aXpYTF9FbWZDMm0tbVc0Ym12ZWN5ajFRY3huZXJNRjFkb2dEVndSTUhsLWRBc19xdi1FUy1GVnpibDFRIIEC; bili_jct=c50413b08d38cb7dc2f40ca8ce5b2957; buvid_fp=0116960deda650739eb876fc011d5f37; bsource=search_bing; home_feed_column=5; browser_resolution=1707-809; bp_video_offset_11991721=904612935399112711; sid=7d1fnl8f; b_lsid=87569C4C_18E03DAC243"
    cookies = []
    for item in cookies_str.split(";"):
        parts = item.strip().split("=")
        if len(parts) < 2:
            continue
        name, value = parts
        cookies.append({"name": name, "value": value})
    return cookies


###获取目标url###
def target_url(id):
    option = webdriver.ChromeOptions()
    option.add_argument("--ignore-certificate-errors")

    driver = swd.Chrome(chrome_options=option)
    # 访问网页
    driver.get("https://www.bilibili.com/")
    print("正在登录b站...")
    # 用cookies登录b站

    # 现在你可以像之前一样使用这些 cookies
    for cookie in get_cookies():
        driver.add_cookie(cookie)
    # 登录后等待一段时间，让页面加载完成
    time.sleep(15)

    # 尝试获取用户名元素
    print("登陆成功")
    url = f"https://www.bilibili.com/read/cv{id}/?from=category_1.top_right_bar_window_history.content.click"

    driver.get(url)

    # 等待一些时间，以确保页面加载完成（你可以根据需要使用等待条件）
    time.sleep(5)
    UrlList = []
    url_pattern = r"https?://[^\s/$.?#].[^\s]*\/main\?[^\s]*"
    print("开始滚动滚动条")
    scroll(driver)
    time.sleep(10)  # 等待一些时间，以确保页面刷新完成
    xhr_requests = driver.requests
    for request in xhr_requests:
        if re.search(url_pattern, request.url):
            print("匹配到正确的url")
            print(request.url)
            if request.url not in UrlList:
                print("添加url")
                UrlList.append(request.url)
    driver.quit()
    print(UrlList)
    return UrlList


###时间戳转换###
def trans_date(v_timestamp):
    timeArray = time.localtime(v_timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


###获取数据###
def get_data(url):
    cookies = get_cookies()[0]
    data = []
    response = requests.get(url, headers=request_header())
    print(response.status_code)
    if response.status_code == 200:
        json_response = response.json()
        replies = json_response["data"]["replies"]
        # 将 replies 保存为 JSON 文件
        # with open(f'data.json', 'w', encoding='utf-8') as f:
        # json.dump(replies, f, ensure_ascii=False, indent=4)
        data.append(replies)
    else:
        print("请求错误")
    time.sleep(1)

    return data


# 将文件写入csv中
def write_to_csv(data, csv_file_path):
    comments_data = [["用户名", "性别", "个性签名", "评论时间", "点赞数", "内容"]]
    for replies in data:
        print("正在读取第" + str(data.index(replies) + 1) + "个网址")
        for reply in replies:
            uname = reply["member"]["uname"]
            sex = reply["member"]["sex"]
            sign = reply["member"]["sign"]
            time1 = trans_date(reply["ctime"])
            like = reply["like"]
            content = reply["content"]["message"]
            comments_data.append([uname, sex, sign, time1, like, content])

    # 创建一个DataFrame
    df = pd.DataFrame(comments_data)

    # 将DataFrame写入CSV文件
    df.to_csv(csv_file_path, index=False, header=False, encoding="utf_8_sig")

    print(f"正在写入数据进 {csv_file_path}")


if __name__ == "__main__":
    # cidName_li = ["动画", "游戏", "影视", "生活", "兴趣", "轻小说", "科技", "笔记"]
    # cidName_li = ["动画"]
    # id_url_dict = {}
    # for i in range(len(cidName_li)):
    #     csv_file = f"Data\{cidName_li[i]}.csv"
    #     print(csv_file)
    #     with open(csv_file, "r", newline="", encoding="utf-8") as file:
    #         reader = csv.reader(file)
    #         # 跳过标题行（如果存在）
    #         next(reader, None)  # 这会读取第一行（即标题行）并跳过它
    #         # 逐行读取CSV文件
    #         for row in reader:
    #             if row:  # 确保行不为空
    #                 # 假设第一列是ID，最后一列是View URL
    #                 id = row[0]
    #                 view_url = row[-1]
    #                 id_url_dict[id] = view_url
    #     # 打印字典内容来验证
    #     for id, url in id_url_dict.items():
    #         print(f"开始爬取ID为{id}的文章")
    #         UrlList = target_url(id)
    #         folder_name = f"Data/{cidName_li[i]}_评论"
    #         file_name = f"{folder_name}/{id}_comments.txt"
    #         # 使用os.makedirs创建目录，exist_ok=True表示如果目录已经存在不会抛出异常
    #         os.makedirs(folder_name, exist_ok=True)
    #         data = get_data(UrlList)
    #         write_to_csv(data, file_name)
    #         print("写入完成")
    data = get_data(
        "https://api.bilibili.com/x/v2/reply/wbi/main?next=0&type=12&oid=31793668&mode=3&plat=1&web_location=1315875&gaia_source=Athena&w_rid=810ef80388becba111f16f4d238c8777&wts=1709464059"
    )
    file_name = f"comments.csv"
    write_to_csv(data, file_name)
