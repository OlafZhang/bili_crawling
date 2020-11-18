#coding=utf-8
#必须确保sql文件是UTF-8编码！
import time,os,pymysql,sys,datetime
db = pymysql.connect("localhost","root","114514","bili" )
count = 0
mask_no = 0
task_session = 0
mask = ["-","/","|","\\"]
start_sec = datetime.datetime.now()
while True:
    if len(sys.argv) != 2:
        print("使用方法：Python +脚本名+数据库文件位置")
        print("请重试")
        time.sleep(3)
        break
    else:
        sql_file = (sys.argv[1])
        with open(sql_file,'r',encoding='utf-8') as f:
            for line in f:
                try:
                    if task_session % 50 == 0:
                        if mask_no == len(mask) - 1:
                            mask_no = 0
                        else:
                            mask_no += 1
                    else:
                        pass
                    wirte_uid = db.cursor()
                    text = str(line)
                    wirte_uid.execute(text)
                    loading_info = str(("\n[%s]Inputing...%s")%(mask[mask_no],task_session))
                    display = str(text + loading_info.replace("\n",""))
                    print(display,end = "")
                    print("\b" * (len(display)*2),end = "",flush=True)
                    db.commit()
                    task_session += 1
                except Exception:
                    db.rollback()
        end_sec = datetime.datetime.now()
        used_time = str((end_sec - start_sec).seconds)
        print("\n")
        print(("Input:%s, used %s secs.")%(task_session,used_time))
        try:
            speed = int(task_session) / int(used_time)
        except ZeroDivisionError:
            speed = 0
        print(("Speed: %s per secs.")%(speed))
        time.sleep(3)
        break
                  
                
            
