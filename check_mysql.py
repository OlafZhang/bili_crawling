# 在数据库随机抽查
import pymysql
import random
db = pymysql.connect("localhost", "root", "114514", "bili")
start = 1
end = 2500000
def part_scan():
    for id in range(start,end,100000):
        print(("Range:%s - %s") % (id,id + 100000))
        for time in range(0,10):
            choice_id = random.randint(id,id + 100000)
            find_uid = db.cursor()
            data_exist = find_uid.execute("select * from bili_user where UID = " + str(choice_id))
            if data_exist == 1:
                print("%s is existed" % choice_id)
                find_uid.close()
                pass
            else:
                print("%s is not existed" % choice_id)
                find_uid.close()
                break

part_scan()