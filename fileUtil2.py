# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 11:21
# @Author  : zhangyx
# @FileName: fileUtil2.py
# @Software: PyCharm

import os
import re
import fileUtil
#数据文件夹路径
filePath='D:\\nlp\\codeCom\\new\\'
#合并后的数据文件保存路径
savePath='D:\\nlp\\codeCom\\datagit\\'
#合并后的数据文件名称
saveFile='merge.txt'
isExists=os.path.exists(savePath)
if not isExists:
    os.makedirs(savePath)

def save(line):
    with open(saveFile, 'a', encoding='utf-8') as save:
        save.write(line)

filename='test.txt'
with open(filename, 'r', encoding="utf-8") as file:
    for line in file:
        #处理
        # print('-----------------------------------------------------')
        # print(line)
        # p0=re.compile("\n", re.S)
        if re.search('\S', line) is None:
            continue
        print(re.search("[(].*[\n][\r\n]", line))
        print("end")
        temp=fileUtil.deletePrint(fileUtil.deleteComment(fileUtil.onlyASCII(line)))
        temp1=fileUtil.mult2one(temp)
        temp2=fileUtil.matchIdentation(temp1)
        # print(temp2)
        save(temp2)

