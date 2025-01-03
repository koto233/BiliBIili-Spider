import csv
import os
import pickle
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
import time


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


# def get_id():
#     cidName_li = ["动画", "游戏", "影视", "生活", "兴趣", "轻小说", "科技", "笔记"]
#     # cidName_li = ["动画"]
#     id_li = []
#     data_folder_name = f"Data\总览数据"
#     os.makedirs(data_folder_name, exist_ok=True)
#     for i in range(len(cidName_li)):
#         csv_file = f"{data_folder_name}\{cidName_li[i]}.csv"
#         print(csv_file)
#         with open(csv_file, "r", newline="", encoding="utf-8") as file:
#             reader = csv.reader(file)
#             # 跳过标题行（如果存在）
#             next(reader, None)  # 这会读取第一行（即标题行）并跳过它
#             # 逐行读取CSV文件
#             for row in reader:
#                 if row:  # 确保行不为空
#                     # 假设第一列是ID，最后一列是View URL
#                     id_li.append(row[0])

#     return id_li


# 将文件写入csv中
def write_to_csv(data, csv_file_path):
    comments_data = [["用户名", "性别", "点赞数", "内容"]]
    for replies in data:
        for reply in replies:
            uname = reply["member"]["uname"]
            sex = reply["member"]["sex"]
            like = reply["like"]
            content = reply["content"]["message"]
            comments_data.append([uname, sex, like, content])

    # 创建一个DataFrame
    df = pd.DataFrame(comments_data)

    # 将DataFrame写入CSV文件
    df.to_csv(csv_file_path, index=False, header=False, encoding="utf_8_sig")

    print(f"正在写入数据进 {csv_file_path}")

def count_page(json_data):
    try:
        count = json_data["data"]["page"]["count"]
        size = json_data["data"]["page"]["size"]
        page = count // size + 1
        if(count==0):
            print("本次数据没有评论")
            return 0
        print(f"本次数据专栏评论有{page}页,共{count}条评论")
    except:
        print("本次数据不存在或已被删除")
        return 0
    return page


def Get_Comment(oid, file_name):
    cookies_dict = {cookie["name"]: cookie["value"] for cookie in get_cookies()}
    # 评论页数
    pn = 1
    # 排序种类 0是按时间排序 2是按热度排序
    sort = 2
    data = []
    while True:
        url = (
            f"https://api.bilibili.com/x/v2/reply?pn={pn}&type=12&oid={oid}&sort={sort}"
        )
        reponse = requests.get(url, headers=Request_Header(), cookies=cookies_dict)
        if reponse.status_code != 200:
            print("网站请求失败")
        try:
            json_data = json.loads(reponse.text)
        except:
            print("获取json失败")
        if pn == 1:
            page=count_page(json_data)
            if(page==0):
                break              
        try:
            replies = json_data["data"]["replies"]
        except:
            print("数据为空")
        for comment in replies:
            if comment.get('replies'):
                rp_id = comment.get('rpid')
                print(f"获取rpid为{rp_id}子评论")
                rp_page=1
                while True: 
                    rp_num = 10
                    reply_url = f'https://api.bilibili.com/x/v2/reply/reply?' + \
                                f'type=12&pn={rp_page}&oid={oid}&ps={rp_num}&root={rp_id}'
                    print(reply_url)
                    reply_response =  requests.get(reply_url, headers=Request_Header(), cookies=cookies_dict)
                    reply_reply = json.loads(reply_response.text) 
                    if(rp_page==1):
                        max_page=count_page(reply_reply)
                        if(max_page == 0):
                            break   
                    reply_reply = reply_reply.get('data').get('replies')  
                    # print(f"{rp_id}获取到rp_id的子评论\n{reply_reply}")
                    if reply_reply is None:
                        break
                    for r in reply_reply:  
                        replies.append(r)
                    rp_page += 1         
                    if(rp_page>max_page):
                        break                       
        print(f"获取到评论{replies}")
        data.append(replies)
        write_to_csv(data, file_name)

        if pn != page:
            pn += 1
        else:
            break


def main():
    cidName_li = ["动画", "游戏", "影视", "生活", "兴趣", "轻小说", "科技", "笔记"]
    # cidName_li = ["动画"]
    id_url_dict = {}
    data_folder_name = f"Data\总览数据"
    os.makedirs(data_folder_name, exist_ok=True)
    for i in range(len(cidName_li)):
        csv_file = f"{data_folder_name}\{cidName_li[i]}.csv"
        print(f"读取文件{csv_file}")
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
            folder_name = f"Data\评论\{cidName_li[i]}_评论"
            file_name = f"{folder_name}\{id}_comments.csv"
            os.makedirs(folder_name, exist_ok=True)
            Get_Comment(id, file_name)


if __name__ == "__main__":
    main()


