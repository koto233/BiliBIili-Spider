from random import choice
import random
import time
import requests
from bs4 import BeautifulSoup
import pymysql as pymysql
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


def Get_Url(cid, sort):
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
        sort(int) : 排序方式
    Returns:
        string: 网址
    """
    url = (
        "https://api.bilibili.com/x/article/recommends?cid="
        + cid
        + "&pn=1&ps=200&jsonp=jsonp&aids=&sort="
        + sort
    )
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
        for sortName, sort in sort_dic.items():
            print(
                f"---------本轮爬取开始,爬取种类为{cidName},排序为{sortName}的专栏-------"
            )
            url = Get_Url(cid, sort)
            print(url)
            req = requests.get(url=url, headers=Request_Header(), timeout=10).text
            reqs = req.replace("fetchJSON_comment98(", "").strip(");")
            data = json.loads(reqs)
            print(f"获取到数据{data}")
            # # 从数据中提取id和stats
            # with open(f"Data\{cidName}_{sortName}.txt", "w", encoding="utf-8") as file:
            #     # 遍历data中的"data"列表
            #     for item in data["data"]:
            #         # 获取id
            #         id = item["id"]
            #         title = item["title"]
            #         summary = item["summary"]
            #         # 获取stats
            #         stats = item["stats"]
            #         # 写入id到文件
            #         file.write(f"ID: {id}\n")
            #         file.write(f"title: {title}\n")
            #         file.write(f"summary: {summary}\n")
            #         # 遍历stats字典，并将每个键值对写入文件
            #         for key, value in stats.items():
            #             file.write(f"{key}: {value}\n")
            #         # 在每个数据项之后添加一个分隔符（例如一行空行），使文件更易读
            #         file.write("\n")

            # 指定CSV文件路径
            csv_file_path = f"Data\{cidName}_{sortName}.csv"
            # 打开（或创建）CSV文件，并设置写入模式
            with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
                # 创建csv写入器对象
                csv_writer = csv.writer(file)
                # 写入表头
                csv_writer.writerow(
                    ["ID", "Title", "Summary"]
                    + ["Stats_" + key for key in data["data"][0]["stats"].keys()]
                )
                # 遍历data中的"data"列表
                for item in data["data"]:
                    # 提取所需数据
                    id = item["id"]
                    title = item["title"]
                    summary = item["summary"]
                    stats_values = list(item["stats"].values())
                    # 写入CSV文件
                    csv_writer.writerow([id, title, summary] + stats_values)
            print("数据已保存到 extracted_data.txt 文件中。")
            print("---------本轮爬取结束-------")
            print("---------开始随机延时-------")
            time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    Get_Json()
