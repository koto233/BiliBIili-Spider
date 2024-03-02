from crawling_product_content import crawl_main
from getdb import get_product_list_from_db
import time
import random
from ip_proxy import structure_proxy
import requests


def main():
    proxies = structure_proxy()
    # proxies = None
    # print(proxies)
    url = 'http://httpbin.org/ip'
    res = requests.get(url=url, proxies=proxies)
    print("目前代理ip为"+str(res.text))
    # proxies = None

    start_num = 2205
    current_num = start_num
    product_list = get_product_list_from_db()
    print("正在获取商品id列表数据")
    # print(product_list)
    for product in product_list:
        if (product[0] < start_num):
            continue
        else:
            print("正在爬取id为"+str(product[1])+"的商品评论")
            sucess = crawl_main(product[1], 1, proxies)
            print(sucess)
            if sucess < 0:
                print("ip被封结束位置序号"+str(current_num))
                break
            print("该商品爬取结束随机延时后继续---序号:"+str(current_num))
            time.sleep(random.randint(1, 3))
            current_num += 1


if __name__ == '__main__':
    main()
