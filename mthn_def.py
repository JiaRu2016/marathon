#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
爬取环校跑成绩
输入: 参赛号,
输出: 姓名,成绩,排名

Version 2.0  写成函数形式
'''

import requests
import re


def GetTrueUrl(num):
    '''
    :param num: 参赛号, 整数型
    :return: 真实的成绩查询地址
    '''
    url = "http://p.thejoyrun.com/201602/university/chengji_chaxunapi.jsp"   # 表单发送的地址
    form_data = {"cansai": str(num), "school":"xmdx"}       # 提交的表单
    res = requests.post(url=url, data=form_data)  # 拿到响应结果

    # 找网址
    txt = res.text.strip()
    txt1 = re.sub(pattern="<script>window.location.href='|'; </script>", repl="", string=txt)
    url_final = "http://p.thejoyrun.com" + txt1

    return url_final


# 写文件
a = 2000
b = 3001
filename = "urls_" + str(a) + "_" + str(b) + ".txt"

with open(filename, 'w') as f:
    for i in range(a,b):
        f.write(str(i) + "\t" + GetTrueUrl(i))
        f.write("\n")
        print(i)

