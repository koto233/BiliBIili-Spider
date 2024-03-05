import csv
import pickle
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
    with open("Data\登录文件\cookies文件.pickle",'rb') as file:
        cookiesList = pickle.load(file)
    return cookiesList



###获取目标url###
def target_url(id):
    # with open("Data\登录文件\cookies文件.pickle",'rb') as file:
    #     cookiesList = pickle.load(file)
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
  
    cookies_dict = {cookie['name']: cookie['value'] for cookie in get_cookies()}
    data = []
    response = requests.get(url, headers=request_header(),cookies=cookies_dict)
    print(response.status_code)
    if response.status_code == 200:
        json_response = response.json()
        try:
            replies = json_response["data"]["replies"]
            data.append(replies)
        except:
            print("返回数据为空")
    else:
        print("请求错误")
    time.sleep(1)

    return data


# 将文件写入csv中
def write_to_csv(data, csv_file_path):
    comments_data = [["用户名", "性别", "评论时间", "点赞数", "内容"]]
    for replies in data:
        print("正在读取第" + str(data.index(replies) + 1) + "个网址")
        for reply in replies:
            uname = reply["member"]["uname"]
            sex = reply["member"]["sex"]
            time1 = trans_date(reply["ctime"])
            like = reply["like"]
            content = reply["content"]["message"]
            comments_data.append([uname, sex,  time1, like, content])

    # 创建一个DataFrame
    df = pd.DataFrame(comments_data)

    # 将DataFrame写入CSV文件
    df.to_csv(csv_file_path, index=False, header=False, encoding="utf_8_sig")

    print(f"正在写入数据进 {csv_file_path}")


if __name__ == "__main__":
    cidName_li = ["动画", "游戏", "影视", "生活", "兴趣", "轻小说", "科技", "笔记"]
    cidName_li = ["动画"]
    id_url_dict = {}
    data_folder_name=f"Data\总览数据"
    os.makedirs(data_folder_name, exist_ok=True)
    for i in range(len(cidName_li)):
        csv_file = f"{data_folder_name}\{cidName_li[i]}.csv"
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
            print(f"开始爬取ID为{id}的文章")
            UrlList = target_url(id)
            data_folder_name=f"Data\评论\{cidName_li[i]}"
            os.makedirs(data_folder_name, exist_ok=True)
            folder_name = f"Data\评论\{cidName_li[i]}_评论"
            file_name = f"{folder_name}\{id}_comments.csv"
            os.makedirs(folder_name, exist_ok=True)
            for apiurl in UrlList:
                data = get_data(apiurl)
                if(len(data)==0):
                    print("本页评论为0")
                    continue
                write_to_csv(data, file_name)
                print("写入完成")


    # data = get_data(
    #     "https://api.bilibili.com/x/v2/reply/wbi/main?next=0&type=12&oid=31793668&mode=3&plat=1&web_location=1315875&gaia_source=Athena&w_rid=810ef80388becba111f16f4d238c8777&wts=1709464059"
    # )
    # file_name = f"comments.csv"
    # write_to_csv(data, file_name)
