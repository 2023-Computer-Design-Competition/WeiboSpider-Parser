# -*- coding: utf-8 -*-
# @Time    : 2023/4/5 11:19
# @Author  : TimDiana
# @FileName: mid_to_url.py
# @Software: PyCharm
with open('topic_mid.txt', 'r') as f:
    lines = f.readlines()

with open('topic_mid_url.txt', 'w') as f:
    for line in lines:
        line = 'https://weibo.com/ajax/statuses/show?id=' + line.strip()
        f.write(line + '\n')
