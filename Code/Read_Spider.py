import os
from random import choice
import random
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import csv


def Request_Header():
    """_summary_
    浏览器请求头伪装
        Returns:
            {}: 浏览器请求头
    """
    headers = {"User-Agent": UserAgent().random}

    return headers


def Get_Url(cid, pn, sort):
    """_summary_
    地址规则 https://api.bilibili.com/x/article/recommends?cid=2&pn=1&ps=20&jsonp=jsonp&aids=&sort=1
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
    url = f"https://api.bilibili.com/x/article/recommends?cid={cid}&pn={pn}&ps=20&jsonp=jsonp&aids=&sort={sort}"
    return url


def Get_Json():
    cid_dic = {
        "动画": "2",
        "游戏": "1",
        "影视": "28",
        "生活": "3",
        "兴趣": "29",
        "轻小说": "16",
        "科技": "17",
        "笔记": "41",
    }
    sort_dic = {
        "投稿时间排序": "1",
        "点赞数最多": "2",
        "评论数最多": "3",
        "收藏数最多": "4",
    }
    for cidName, cid in cid_dic.items():
        print(f"---------本轮爬取开始,爬取分区为{cidName}的专栏-------")
        for sortName, sort in sort_dic.items():
            print(f"---------按照{sortName}排序-------")
            for i in range(1, 99):
                print(f"---------正在爬取第{str(i)}页-------{cidName}")
                url = Get_Url(cid, str(i), sort)
                print(url)
                req = requests.get(url=url, headers=Request_Header(), timeout=10).text
                reqs = req.replace("fetchJSON_comment98(", "").strip(");")
                data = json.loads(reqs)
                if len(data["data"]) == 0:
                    print(f"按照{sortName}排序的{cidName}分区的专栏爬取结束，一共{i}页")
                    continue
                print(f"获取到数据{data}")
                data_folder_name = f"Data\总览数据"
                os.makedirs(data_folder_name, exist_ok=True)
                # CSV文件的名称和路径
                csv_file = f"{data_folder_name}\{cidName}.csv"
                # CSV文件的表头
                headers = [
                    "ID",
                    "Title",
                    "View",
                    "Favorite",
                    "Like",
                    "Dislike",
                    "Reply",
                    "Share",
                    "Coin",
                    "Dynamic",
                    "View URL",
                ]
                # 根据是否是第一页选择文件打开模式
                mode = "w" if i == 1 else "a"
                header_mode = True if i == 1 else False
                with open(csv_file, mode, newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    # 如果是第一页，写入表头
                    if header_mode:
                        writer.writerow(headers)
                    # 遍历数据项，提取信息并写入CSV
                    for item in data["data"]:
                        row = [
                            item["id"],
                            item["title"],
                            item["stats"]["view"],
                            item["stats"]["favorite"],
                            item["stats"]["like"],
                            item["stats"]["dislike"],
                            item["stats"]["reply"],
                            item["stats"]["share"],
                            item["stats"]["coin"],
                            item["stats"]["dynamic"],
                            item["view_url"],
                        ]
                        writer.writerow(row)
                print("数据保存到CSV完成。")
                print(f"---------第{i}页爬取结束-------")
                print("---------开始随机延时-------")
                time.sleep(random.randint(1, 3))
            print(f"---------按照{sortName}排序的{cidName}分区爬取结束-------")
        print(f"---------{cidName}分区爬取结束-------")


if __name__ == "__main__":
    Get_Json()
