#这是一个同步工具,也可以当导出工具使用
#本端和从属端出现数据冲突时，回收所有的sql文件，导入后再来跑这个代码
#他会把已经导入的数据导出，再次分发后爬取进度将同步

import requests,time,traceback,os
import pymysql,datetime
db = pymysql.connect("localhost","root","114514","bili" )

start = 1
end = 2500001

file_name = str(("mysql_from_%s_to_%s.sql")%(str(start),str(end)))

list_uid = []

mask_no = 0

task_session = 0

mask = ["-","/","|","\\"]

user_total = end - start + 1

for i in range(int(start),int(end) + 1):
        list_uid.append(int(i))

start_sec = datetime.datetime.now()
for id in list_uid:
    find_uid = db.cursor()
    data_exist = find_uid.execute("select * from bili_user where UID = " + str(id))
    if data_exist == 0:
        pass
    else:
        name = ""
        
        info_list = list(find_uid.fetchall()[0])
        
        uid = str(info_list[0])
        temp = uid.split("'")
        uid = temp[0]
        
        raw_name = str(info_list[1])

        for i in range(0,len(raw_name)):
            if raw_name[i] == str("\\"):
                name += "\\"
            else:
                pass
                name += raw_name[i]
        
        follower = str(info_list[2])
        temp = follower.split("'")
        follower = temp[0]

        following = str(info_list[3])
        temp = following.split("'")
        following = temp[0]

        up_100 = str(info_list[4])
        if task_session % 50 == 0:
            if mask_no == len(mask) - 1:
                mask_no = 0
            else:
                mask_no += 1
        else:
            pass
        into_command = str(("insert into bili_user values(%s,'%s',%s,%s,%s);")%(uid,name,follower,following,up_100))
        loading_info = str(("\n[%s]Outputing...%s/%s")%(mask[mask_no],task_session,user_total))
        print(into_command,end = "")
        print(loading_info,end = "")
        print("\b" * (len(into_command)*2),end = "",flush=True)
        file = open(file_name, 'a', encoding='utf-8')
        file.write(into_command + "\n")
        file.close()
        task_session += 1
    find_uid.close()
end_sec = datetime.datetime.now()
used_time = str((end_sec - start_sec).seconds)
print("\n")
print(("Output:%s, used %s secs.")%(task_session,used_time))
try:
        speed = int(task_session) / int(used_time)
except ZeroDivisionError:
        speed = 0
print(("Speed: %s per secs.")%(speed))
time.sleep(3)
    
