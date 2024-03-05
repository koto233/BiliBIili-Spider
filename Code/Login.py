import os
from selenium import webdriver
import time
import pickle


def Get_Cookies():
    folder_name = "Data\登录文件"
    cookies_file_name = f"{folder_name}\cookies文件.pickle"
    os.makedirs(folder_name, exist_ok=True)
    browser = webdriver.Chrome()

    browser.get("https://www.bilibili.com/")

    time.sleep(5)

    print("字典长度:\n", len(browser.get_cookies()), browser.get_cookies())

    input("请输入任意键继续...")

    time.sleep(5)

    with open(cookies_file_name, "wb") as file:

        pickle.dump(browser.get_cookies(), file)

    print("字典长度:\n", len(browser.get_cookies()), browser.get_cookies())

    input("请输入任意键继续...")

    browser.delete_all_cookies()

    time.sleep(5)

    print("字典长度:\n", len(browser.get_cookies()), browser.get_cookies())


if __name__ == "__main__":
    Get_Cookies()
