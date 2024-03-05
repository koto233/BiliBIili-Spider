import pickle
from browsermobproxy import Server
from selenium import webdriver





with open("Data\登录文件\cookies文件.pickle",'rb') as file:
    cookiesList = pickle.load(file)

print(cookiesList)



