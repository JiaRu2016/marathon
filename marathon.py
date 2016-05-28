#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
爬取环校跑成绩
输入: 参赛号,
输出: 姓名,成绩,排名

Version 1.0
'''


################################################################################
# Part I
# 构造最终成绩查询网址
################################################################################


num = 2637
numstr = str(num)

import requests
import re

url = "http://p.thejoyrun.com/201602/university/chengji_chaxunapi.jsp"
form_data = {"cansai": numstr, "school":"xmdx"}
res = requests.post(url=url, data=form_data)
txt = res.text

# txt is like this :
# <script>window.location.href='/201602/university/share.jsp?uuid=371130e517ce4f72bf1eecc482bc7c85&school=xmdx'; </script>
# 发现其中的
# href='/201602/university/share.jsp?uuid=371130e517ce4f72bf1eecc482bc7c85&school=xmdx'
# 才是真正成绩查询的网址, 这里面的uuid实际上是表单中参赛号?

# 正则表达式提取txt中间的 '/201602/university/share.jsp?uuid=371130e517ce4f72bf1eecc482bc7c85&school=xmdx'
txt1 = re.sub(pattern="<script>window.location.href='", repl="", string=txt)
txt2 = re.sub(pattern="'; </script>", repl="", string=txt1)

# 构造真实成绩查询网址
url_final = "http://p.thejoyrun.com" + txt2



# 测试

if __name__=="__main__":
    print(url_final)  # 验证网址是否有效


with open('marathon/num_url.txt', '') as f:
    f.write(numstr)
    f.write("\t")
    f.write(url_final)
    f.write("\n")


################################################################################
# Part II
# 发现查询网址是一个jsp动态网页, 用selenuim模拟浏览器行为获取信息,比较慢...
# 可是为什么R可以直接解析出来......不懂...
################################################################################


'''
# 以下代码废弃....发现可以用R搞.. (╯‵□′)╯︵┻━┻

from selenium import webdriver
import time

# 1. 打开Chrome浏览器
# 括号里的内容是ChromeDriver的路径
dr = webdriver.Chrome('/Users/jiaru2014/Desktop/chromedriver')

# 2. 输入网址
dr.get(url_final)

# 3. 找 player, time, rank
player = dr.find_element_by_class_name("name").text
time = dr.find_element_by_class_name("time").text
rank = dr.find_element_by_class_name("ranking").text

# 测试
print(player)
print("时间:", time, sep=" ")
print("排名:", rank, sep=" ")

'''
