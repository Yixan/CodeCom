import sqlite3
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
# sql = 'CREATE TABLE Grame1 (id integer PRIMARY KEY autoincrement, Pro  varchar(100), Word varchar(100),Third varchar(100))'
# cursor.execute(sql)
# file=open('1_grams.txt','w',)
# with open('3grams.txt','r',encoding='gbk') as f:
#     for line in f:
#         if line=='1grams'+'\n':
#             continue
#         if line=='111111111111111111111111\n':
#             break
#         content=line.strip().split()
#         # print(content)
#         if(len(content)<3):
#             for i in range(len(content)-1,3):
#                 content.append('None')
#                 # print(content)
#         file.write(content[0]+'\t'+content[1]+'\t'+content[2]+'\n')
# file.close()

with open('1_grams.txt','r',encoding='gbk') as f:
# decode('gbk').
#     i=0
# sqllist=[]
    for line in f.readlines():
        content=line.encode("gbk").decode("utf-8").strip().split()
        pass
        # sql1 = "insert into order_log values(null,%s,%s,%s)" % (content[0],content[1], content[2])
        temp = "insert into Grame1(id, Pro,Word,Third)  values(null,%s,%s,%s)"
        args=("{}".format(content[0]),"{}".format(content[1]),"{}".format(content[2]))
        # sql1 = "insert into Grame1(id, Pro,Word,Third)  values(null,'s','s','s')"
        sql_i = temp % args
        # sqllist.append(sql_i)
        print(sql_i)
        print(args)
        cursor.execute(temp,args)
        # print(sql_i)
        conn.commit()