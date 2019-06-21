# -*- coding: utf-8 -*-
# @Time    : 2019/5/21 17:43
# @Author  : zhangyx
# @FileName: examineCode.py
# @Software: PyCharm

import calBleu
import astor
import ast
def examineCode(code):
    try:
        node = ast.parse(code)
        print(astor.to_source(node))
        return True
    except SyntaxError as e:
        print(e)
        return False

def examineCodeFile(code_file):
    try:
        node = astor.parse_file(code_file)
        print(astor.to_source(node))
        return True
    except SyntaxError as e:
        print(e)
        return False

def BLEU(data_file,model='file'):
    pass
    if not examineCodeFile(data_file):
        print("不符合语法规范")
        return 0
    return calBleu.calBLEU(data_file)