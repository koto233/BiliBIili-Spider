import time
import requests
from lxml import etree
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import random
cookie = 'shshshfpa=b3339eaa-35ee-5e5a-05ed-5b95dda79ce4-1668402431; shshshfpb=d_dKbXMFJP_C-rqTmcI9f3Q; o2State={%22webp%22:true%2C%22avif%22:false}; pinId=ujseVVomJXqAIYJMM1uFiw; TrackID=1AALF0PgGOe1M57-hYUpkAbUvT9G7gMVCnSUS6F1edmrlrtF-W_POOYFA4qEKSCvAavQFOpuPKc_jAii6_mpHx0twMFgmeKcCSaua94zj03NC0Utc0oEfR4rKsPVPgGcH; shshshfpx=b3339eaa-35ee-5e5a-05ed-5b95dda79ce4-1668402431; unpl=JF8EAKtnNSttDxgGUh0CTBYYSg9SW18AHh5WbmVQVF4KT10CEgFMEBl7XlVdXxRKFB9sZxRUXVNOUg4fBCsSEHteVVxeCU8WAmpiNWRYW0xTBCsBGyIRe11TWVQNShQGbGEAUltYTFcHHwYaFxV7XGReVQ97FwJuZgZVXF9IVgcfMisTIEptVW4LZksWAm5mBFFdW0kZBRwFEhcRSFhXWFgOTRcEbGUBUFxdTmQEKwE; __jdv=76161171|cn.bing.com|-|referral|-|1679368109562; PCSYCityID=CN_510000_511500_0; areaId=22; pin=a1768733431; unick=%E6%9C%88%E4%B8%8B%E8%8A%B1%E8%A7%81%E6%80%A5%E8%A1%8C; _tp=HcbkVdQLuDoUZM5ysk3ltA%3D%3D; _pst=a1768733431; ipLoc-djd=22-2005-2013-36482; thor=07E3D5B82F601BDD301D1C18ADD06F82EB1AE6F449F67D613CB646B4EEE7D25DBBE48CE7783D02BA44938A99871B87249115111FF21697111C17C48EF379F38E3398F4711ECF0AB8A18C67EACE03DCA2BE901BAE1671C921FD80754DC3BBF8907C4E4D4E8641EE5E9C080A41FE990A2E8FA569A1084E63553417E90216A67AC4B98A9AC212DDD66BD24C41E58DD33348; __jda=76161171.1668402427477162355044.1668402427.1676951277.1679368110.57; __jdc=76161171; user-key=cd62c2a5-8035-4a5f-9e7b-c18b9cd85d44; cn=0; shshshfp=133a3f811019d9c6b4f00b71adebeddc; __jdb=76161171.40.1668402427477162355044|57.1679368110; shshshsID=84cb82d458217ac4c97286277b0e0270_34_1679372679115'


def request_header_login():
    headers = {
        'User-Agent': UserAgent().random,
        'Cookie': 'shshshfpa=b3339eaa-35ee-5e5a-05ed-5b95dda79ce4-1668402431; shshshfpb=d_dKbXMFJP_C-rqTmcI9f3Q; o2State={%22webp%22:true%2C%22avif%22:false}; pinId=ujseVVomJXqAIYJMM1uFiw; TrackID=1AALF0PgGOe1M57-hYUpkAbUvT9G7gMVCnSUS6F1edmrlrtF-W_POOYFA4qEKSCvAavQFOpuPKc_jAii6_mpHx0twMFgmeKcCSaua94zj03NC0Utc0oEfR4rKsPVPgGcH; shshshfpx=b3339eaa-35ee-5e5a-05ed-5b95dda79ce4-1668402431; unpl=JF8EAKtnNSttDxgGUh0CTBYYSg9SW18AHh5WbmVQVF4KT10CEgFMEBl7XlVdXxRKFB9sZxRUXVNOUg4fBCsSEHteVVxeCU8WAmpiNWRYW0xTBCsBGyIRe11TWVQNShQGbGEAUltYTFcHHwYaFxV7XGReVQ97FwJuZgZVXF9IVgcfMisTIEptVW4LZksWAm5mBFFdW0kZBRwFEhcRSFhXWFgOTRcEbGUBUFxdTmQEKwE; __jdv=76161171|cn.bing.com|-|referral|-|1679368109562; PCSYCityID=CN_510000_511500_0; areaId=22; pin=a1768733431; unick=%E6%9C%88%E4%B8%8B%E8%8A%B1%E8%A7%81%E6%80%A5%E8%A1%8C; _tp=HcbkVdQLuDoUZM5ysk3ltA%3D%3D; _pst=a1768733431; ipLoc-djd=22-2005-2013-36482; thor=07E3D5B82F601BDD301D1C18ADD06F82EB1AE6F449F67D613CB646B4EEE7D25DBBE48CE7783D02BA44938A99871B87249115111FF21697111C17C48EF379F38E3398F4711ECF0AB8A18C67EACE03DCA2BE901BAE1671C921FD80754DC3BBF8907C4E4D4E8641EE5E9C080A41FE990A2E8FA569A1084E63553417E90216A67AC4B98A9AC212DDD66BD24C41E58DD33348; __jda=76161171.1668402427477162355044.1668402427.1676951277.1679368110.57; __jdc=76161171; user-key=cd62c2a5-8035-4a5f-9e7b-c18b9cd85d44; cn=0; shshshfp=133a3f811019d9c6b4f00b71adebeddc; __jdb=76161171.40.1668402427477162355044|57.1679368110; shshshsID=84cb82d458217ac4c97286277b0e0270_34_1679372679115'

    }

    return headers


# 浏览器请求头伪装
def request_header():
    headers = {
        'User-Agent': UserAgent().random
    }

    return headers


# 待测试ip列表
all_ip_list = []

# 云代理免费ip


def get_ip():
    for i in range(30, 100):
        url1 = f'http://www.ip3366.net/free/?page={i}'
        url2 = f'http://www.ip3366.net/free/?stype=2&page={i}'
        print(f'----正在抓取第{i}页----')
        res = requests.get(
            url=url1, headers=request_header())
        text = res.text.encode('ISO-8859-1')
        # text = res.text.encode('utf-8')
        # print(text.decode('gbk'))
        # 使用xpath解析，提取出数据ip，端口
        html = etree.HTML(text)
        # print(html)
        tr_list = html.xpath('/html/body/div[2]/div/div[2]/table/tbody/tr')
        for td in tr_list:
            ip_ = td.xpath('./td[1]/text()')[0]  # ip
            port_ = td.xpath('./td[2]/text()')[0]  # 端口
            proxy = ip_ + ':' + port_
            all_ip_list.append(proxy)
            if (test_ip(proxy)):  # 开始检测获取到的ip是否可以使用
                print("获取到可用ip")
                return proxy
                break
    return 0

# 89免费代理


# def get_ip():
#     for i in range(63, 100):
#         time.sleep(random.randint(1, 2))
#         url1 = f'https://www.89ip.cn/index_'+str(i)+'.html'
#         print(f'----正在抓取第{i}页----')
#         res = requests.get(
#             url=url1, headers=request_header()).text
#         soup = BeautifulSoup(res, 'lxml')
#         table = soup.find('table', class_='layui-table')
#         rows = table.find_all('tr')
#         for row in rows[1:]:
#             cells = row.find_all('td')
#             ip = cells[0].text.strip()
#             port = cells[1].text.strip()
#             proxy = ip + ':' + port
#             if (test_ip(proxy)):  # 开始检测获取到的ip是否可以使用
#                 print("获取到可用ip")
#                 return proxy
#                 break
#     return 0


# 检测ip是否可以使用


def test_ip(proxy):
    # 构建代理ip
    proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy,
    }
    try:
        res = requests.get(url='https://www.baidu.com/', headers=request_header(),
                           proxies=proxies, timeout=1)  # 设置timeout，使响应等待1s
        res.close()
        if res.status_code == 200:
            print(proxy, '\033[31m可用\033[0m')
            return 1
        else:
            print(proxy, '不可用')
            return 0
    except:
        print(proxy, '请求异常')
        return 0


def structure_proxy():
    # 获取代理ip
    print("开始获取代理ip")
    proxy = get_ip()
    if (proxy != 0):
        # 构建ip代理
        proxies = {
            "http": "http://" + proxy,
            "https": "http://" + proxy,
        }
        return proxies
    else:
        print("暂无可用ip稍后再试")


if __name__ == '__main__':
    get_ip()
    # test_ip('113.239.154.129:22014')
