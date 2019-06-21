# -*- coding: utf-8 -*-
# @Time    : 2019/5/19 11:19
# @Author  : zhangyx
# @FileName: reparse.py
# @Software: PyCharm

# import fileUtil

# test_str1='acc123你好。】、~!].'
# print(fileUtil.onlyASCII(test_str1))

# test_str2="test#aaaaabbbb\n '''ddd\ncccc'''"
# fileUtil.deleteComment(test_str2)
#
# test_str3="def onlyASCII(data," \
          # "model='string',outputName='result.txt'):"
# fileUtil.deleteParement(test_str3)

# test_str4="111\nprint('----------------')"
# print(fileUtil.deletePrint(test_str4))

# test_str5='data\\1.txt'
# fileUtil.matchIdentation(test_str5,model='file')
# test="fileUtil.matchIdentation[test_str5,\r\nmodel='file',\r\nmodel='file']"
# fileUtil.mult2one(test)
# test1="fileUtil.matchIdentation(test_str5,\r\nmodel='file',\r\nmodel='file')"
# fileUtil.mult2one(test1)
# test2="fileUtil.matchIdentation{test_str5,\r\nmodel='file',\r\nmodel='file'}"
# fileUtil.mult2one(test2)
import ast
import astor
import fileUtil
# ex = ast.parse('2 + 3*4 + x', mode='eval')
#
# def parse_and_export(input_path, output_path):
#     with open(output_path, 'w') as outputs:
#         outputs.write(astor.to_source(astor.parsefile(input_path)))
#     outputs.flush()


# class MyVisitor(ast.NodeVisitor):
#     def visit_Str(self, node):
#         print('Found string "%s"' % node.s)
#         if node.s == "123456":
#             node.s = "45678"
#     def visit_FunctionDef(self, node):
#         print('Found function ', node._fields)

import os,re
filePath='datagit\\'
# node=astor.parse_file('test.txt')
# class RemovePrint(ast.NodeTransformer):
#
#     def visit_Print(self, node):
#         new_node = ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
#             args=node.values,
#             keywords=[], starargs=None, kwargs=None))
#         ast.copy_location(new_node, node)
#         return new_node
#
#
# try:
#     node = RemovePrint().visit(astor.parse_file('fileUtil2.py'))
#     ast.fix_missing_locations(node)
#     # print(ast.dump(node))
#     with open('result.txt', 'w', encoding="utf-8") as f:
#         f.write(astor.to_source(node))
# except SyntaxError as e:
#     print(e)
def reparse(filePath):
    for filename in os.listdir(filePath):
        with open(filePath+filename,'r',encoding='utf-8') as file:
            data=file.read()

        try:
            node = ast.parse(fileUtil.deleteComment(data))
            with open('datagit1\\'+filename, 'w', encoding="utf-8") as f:
                f.write(astor.to_source(node))
        except SyntaxError as e:
            # print(e)
            pass

if __name__=='__main__':
    reparse(filePath)
