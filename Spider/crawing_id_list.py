from random import choice
import random
import time
import requests
from bs4 import BeautifulSoup
import pymysql as pymysql
from ip_proxy import structure_proxy
from ip_proxy import request_header
from ip_proxy import request_header_login
from fake_useragent import UserAgent


# 浏览器请求头伪装
def request_header():
    headers = {
        'User-Agent': UserAgent().random
    }

    return headers


# 开爬
def get_product_list(page, proxy):
    url = 'https://search.jd.com/Search?keyword=%E5%AE%B6%E5%85%B7&psort=4&wq=%E5%AE%B6%E5%85%B7&psort=4&pvid=ecaecc3e9c32493982b596dc12e79da5&page=' + \
        str(page)+'&s=1&click=0'
    # 获取text文本
    webdata = requests.get(url, headers=request_header(),
                           proxies=proxy).text
    # print(webdata)
    # 使用BeautifulSoup解析text文本
    soup = BeautifulSoup(webdata, 'lxml')
    product = soup.select(
        "li.gl-item > div.gl-i-wrap > div.p-name.p-name-type-2 >a>em")
    # print(product)
    cell_id = soup.find_all("li", class_="gl-item")
    # print(cell_id)
    ret_list = []
    # print(cell_id)
    for li_tags, name_tags in zip(cell_id, product):
        # 提取出标题和链接信息
        time.sleep(random.randint(1, 3))
        skuid = li_tags.get("data-sku")

        name = name_tags.text
        name_short = name[:20]
        data = {
            'skuid': skuid,
            'product_name': name_short,
        }
        ret_list.append(data)
    print(ret_list)
    return ret_list


# 爬取指定页数商品id存入数据库
def get_product_list_whole_jd():
    # ip代理
    # proxies = structure_proxy()
    proxies = None
    # 起始页数
    i = 0
    # 结束页数
    n = 20
    while i < n:
        list_data = get_product_list(i, proxies)
        time.sleep(random.randint(0, 3))
        for p in list_data:
            # 获取数据库链接

            connection = pymysql.connect(host="localhost", user="root", passwd="123456", db="jd", port=3306,
                                         charset="utf8")
            try:

                with connection.cursor() as cursor:
                    # 创建sql语句
                    sql = "insert into jd_product (`skuid`, `product_name`) values (%s,%s)"

                    # 执行sql语句
                    cursor.execute(
                        sql, (p['skuid'], p['product_name']))

                    # 提交数据库
                    connection.commit()
            finally:
                connection.close()
        print(time.asctime(time.localtime(time.time())) +
              ": 商品信息第" + str(i + 1) + "页已存入数据库")
        i += 1


if __name__ == '__main__':
    # proxy = None
    get_product_list_whole_jd()
    # get_product_list(1, proxy)
