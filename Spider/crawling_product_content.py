# -*- coding: utf-8 -*-
import json
import time
import random
import pymysql
import requests
from ip_proxy import request_header


def crawlProductComment(url, score, proxies):
    # print(proxies)
    req = requests.get(url=url, headers=request_header(),
                       proxies=proxies, timeout=10).text
    reqs = req.replace("fetchJSON_comment98(", "").strip(');')
    data = json.loads(reqs)
    # print(req)
    comments = data['comments']
    if (score == 3):
        label = '2'
        print('正在爬取好评')
    elif (score == 2):
        label = '1'
        print('正在爬取中评')
    elif (score == 1):
        label = '0'
        print('正在爬取差评')
    if len(data['comments']) == 0:
        print(time.asctime(time.localtime(time.time())) +
              "\nSeems no more data to crawl")
        return -1

    for comment in data['comments']:
        product_name = comment['referenceName']
        content = comment['content']

        print(content)
        # print(label)
        connection = pymysql.connect(
            host="localhost", user="root", passwd="123456", db="jd", port=3306, charset="utf8")
        try:
            # 获取会话指针
            with connection.cursor() as cursor:
                # 创建sql语句
                sql = "insert into jd_content (`productName`,`content`,`label`) values (%s,%s,%s)"
            # 执行sql语句
                cursor.execute(
                    sql, (product_name, content, label))

            # 提交数据库
                connection.commit()
            print("存入数据库成功")
        finally:
            connection.close()
    return 1


def crawl_main(skuid, score, proxies):
    result = 8
    print(result)
    for i in range(0, 10):
        print("正在爬取第"+str(i+1)+"页")
        # 通过更改page参数的值来循环读取多页评论信息
        url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=' + str(
            skuid) + '&score='+str(score)+'&sortType=5&page=' \
            + str(i) + '&pageSize=10&isShadowSku=0&fold=1'
        # print(url)
        try:
            comments = crawlProductComment(url, score, proxies)
        except:
            print('获取网页信息失败，可能是ip被封')
            result = result-1
            # print(result)
            continue
        # crawlProductComment(url, 3, proxies)
        print("随机延时-----")
        time.sleep(random.randint(1, 3))
        print("id为"+str(skuid)+"的商品爬取第"+str(i+1)+"页结束")
    return result


# if __name__ == '__main__':

    # crawl_main(100013307481, 3)
    # crawlProductComment(
    #     'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100013307481&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1')
