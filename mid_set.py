# -*- coding: utf-8 -*-
# @Time    : 2023/3/5 10:56
# @Author  : TimDiana
# @FileName: test.py
# @Software: PyCharm

with open('topic_mid.txt', 'r') as f:
    lines = f.readlines()
s1 = set(lines)
with open('topic_mid.txt', 'w') as f:
    for line in s1:
        f.write(line)
