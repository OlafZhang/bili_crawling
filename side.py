# 注意，虽然会写入文件，但是会从数据库检查，用于二次爬取
# 配置文件将不在此适用，请在这里修改参数
task_default = [1,1000000]
all_task_list = ["task_default"]

import sys
import os
import requests
import time
import datetime
import traceback
import random
import json
import fake_useragent
from colorama import init
import pymysql

print("\033[1;33m[*]Bilibili users info crawling(Side vers.)\033[0m")


gotosleep = False
device = "电脑"
no_sql = False
sql_ip = "localhost"
sql_user = "root"
sql_pass = "123456"
sql_database = "bili"
command = True
sleep_start = 25
sleep_end = 60
shut_time = 1800
stop_mask = False
connect_ok = True
user_id_pick = "NULL"
runtime_task_session = 0

# 初始化IFTTT
def send_notice_ifttt(text1, text2):
    info = str(("来自 %s:%s") % (text1, text2))
    print(("\033[1;31m[*]%s\033[0m") % (info))

send_notice_ifttt(device, "爬取程序已启动。")

db = pymysql.connect(sql_ip, sql_user, sql_pass, sql_database)

print("\033[1;32m[*]Powered by Olaf Zhang.All right reserved.\033[0m")
print("\033[1;36m[*]List tasks.\033[0m")
main_task = 0
all_total = 0
for user_task_list in all_task_list:
    exec("start = int(" + user_task_list + "[0])")
    exec("end = int(" + user_task_list + "[1])")
    total = end - start + 1
    all_total += total
    list_name = user_task_list
    main_task += 1
    print('\033[1;32m[+]Found list %s: Call "%s", from %s to %s, total %s.\033[0m' % (
        main_task, list_name, start, end, total))
print("\033[1;36m[*]List tasks OK, total:%s\033[0m" % all_total)
print("\033[1;36m[*]SleepTime from %s secs to %s secs.\033[0m" % (sleep_start / 10, sleep_end / 10))


def session_main(start, end):
    print("\033[1;33m[*]Range from %s to %s\033[0m" % (str(start), str(end)))
    time.sleep(1)
    global task_session
    global stop_mask
    global retry_time
    retry_time = 10
    global user_id_pick
    global all_task_list
    global sleep_start
    global sleep_end
    global runtime_task_session
    global linux
    for user_task_list in all_task_list:
        exec("global " + user_task_list)
    task_session = 1
    list_uid = []
    print("\033[1;33m[*]Creating list.\033[0m")
    for i in range(int(start), int(end) + 1):
        list_uid.append(int(i))
    for i in range(0, 10):
        random.shuffle(list_uid)
    file_name = str("mysql_from_%s_to_%s.sql" % (str(start), str(end)))
    sql = str(".\\"+ file_name)
    if os.path.exists(sql):
        print("\033[1;33m[*]File existed, now loading...\033[0m")
        pass
    else:
        import pathlib
        pathlib.Path(sql).touch()
        print("\033[1;36m[+]File touched.\033[0m")
    sql_file = open(sql, 'r', encoding='utf-8')
    mask_no = 0
    mask = ["-", "/", "|", "\\"]
    start_sec = datetime.datetime.now()
    for line in sql_file.readlines():
        text = str(line)
        text = text.split('values(')
        text = str(text[1])
        text = text.split(',')
        text = str(text[0])
        if int(text) in list_uid:
            list_uid.remove(int(text))
            task_session += 1
            loading_info = str("\033[1;33m[%s]Loading...%s\033[0m" % (mask[mask_no], task_session))
            if task_session % 1000 == 0:
                if mask_no == len(mask) - 1:
                    mask_no = 0
                else:
                    mask_no += 1
                print(loading_info, end="")
                print("\b" * (len(loading_info) * 2), end="", flush=True)
            else:
                pass
        else:
            pass
    else:
        pass
        end_sec = datetime.datetime.now()
        used_time = str((end_sec - start_sec).seconds)
        print("\033[1;32m[*]Initialization completed:%s, used %s secs.\033[0m" % (task_session, used_time))
        print("\n")
        task_session += 1
        sql_file.close()

    for id in list_uid:
        try:
            global user_id_pick
            user_id_pick = id
            time_now = str(time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime()))
            find_uid = db.cursor()
            data_exist = find_uid.execute("select * from bili_user where UID = " + str(id))

            if data_exist == 0:
                ua_list = fake_useragent.UserAgent()
                ua = ua_list.random
                headers = {"Host": "api.bilibili.com", "User-Agent": str(ua)}
                name = requests.get("https://space.bilibili.com/" + str(id))
                retry_time = 10
                if name.status_code != 200:
                    connect_ok = False
                    st_code = name.status_code
                else:
                    connect_ok = True
                    st_code = 200
                if st_code == 412:
                    print('\033[1;31m[-]Error:' + str(st_code) + '\033[0m')
                    ban_count()
                else:
                    pass
                fans = requests.get("https://api.bilibili.com/x/relation/stat?vmid=" + str(id), headers=headers)
                if full_info:
                    print("\033[1;33m[*]Get info from API.\033[0m")
                else:
                    pass
                fans = fans.json()
                following = fans['data']['following']
                fans = fans['data']['follower']
                try:
                    name = name.text
                    name = name.split('<title>')
                    name = str(name[1])
                    name = name.split('的个人空间 - 哔哩哔哩 ( ゜- ゜)つロ 乾杯~ Bilibili</title>')  ###主要防止某些神经病用特殊的昵称导致爬取异常
                    name = str(name[0])
                except:
                    name = "(##闸总用户##)"
                raw_name = name
                name = ''
                for i in range(0, len(raw_name)):
                    if raw_name[i] == str("\\"):
                        name += "\\"
                    elif raw_name[i] == str("\{"):
                        name += "\{"
                    elif raw_name[i] == str("\}"):
                        name += "\}"
                    else:
                        pass
                    name += raw_name[i]
                sleep_time = random.randint(sleep_start, sleep_end)
                sleep_time = sleep_time / 10
                try:
                    if not connect_ok:
                        name = "(##不存在用户##)"
                    else:
                        pass
                    print("\033[1;36m[+]Task_" + str(task_session) + ":" + str(id) + "(" + str(name) + ") with " + str(
                        fans) + " fan(s) and " + str(following) + " following(s).\033[0m")
                    task_session += 1
                    temp = ""
                    for i in name:
                        if i == "\\":
                            temp += "\\"
                        else:
                            pass
                        temp += i
                    name = temp
                    into_command = str(
                        "insert into bili_user values(" + str(id) + ",'" + str(name) + "'," + str(fans) + "," + str(
                            following) + ",0)")
                    sql_file = open(sql, 'a', encoding='utf-8')
                    sql_file.write(into_command + ";\n")
                    sql_file.close()
                    time.sleep(sleep_time)
                except Exception:
                    db.rollback()
            else:
                print("\033[1;33m[*]Task_%s:%s existed ,skipping.\033[0m" % (task_session, user_id_pick))
                task_session += 1
            runtime_task_session += 1
            retry_time = 10

        except KeyboardInterrupt:
            if no_sql:
                try:
                    print(" ")
                    print("\033[1;31m[!]Keyboard Interrupt detected, now pause.\033[0m")
                    print("\033[1;36m[*]Enter [E]xit or just Enter...\033[0m")
                    user_input = str(input("INPUT_HERE> "))
                    if user_input == str("e") or user_input == str("E") or user_input == str("Exit") or user_input == str("exit"):
                        print("\033[1;31m[!]Exit by user.\033[0m")
                        sys.exit(1)
                        break
                    else:
                        pass
                except KeyboardInterrupt:
                    print(" ")
                    print("\033[1;31m[!]Force exit by user.\033[0m")
                    if linux:
                        pass
                    else:
                        time.sleep(3)
                    sys.exit(1)
                    break
            else:
                print(" ")
                print("\033[1;31m[!]Force exit by user.\033[0m")
                if linux:
                    pass
                else:
                    time.sleep(3)
                sys.exit(1)
                break
        except requests.exceptions.ConnectionError:
            try:
                if retry_time != 1:
                    retry_time -= 1
                    print("\033[1;31m[-]Check your connection, retry time:" + str(retry_time) + "\033[0m")
                    time.sleep(10)
                    print("\033[1;33m[*]Try continue...\033[0m")
                    pass
                else:
                    print("\033[1;31m[-]Quiting...\033[0m")
                    break
            except:
                continue
    stop_mask = True


def ban_count():
    shut_time = 1800
    task_session = 1
    change = True
    for i in range(shut_time, 0, -1):
        shut_time -= 1
        hour = shut_time // 3600
        temp_1 = shut_time % 3600
        minu = temp_1 // 60
        sec = temp_1 % 60
        if change:
            change = False
            info = str("\033[1;31m[-]Banding now, change IP or Waiting ,ETA: %dmin %dsec.\033[0m" % (minu, sec))
        else:
            change = True
            info = str("\033[1;31m[*]Banding now, change IP or Waiting ,ETA: %dmin %dsec.\033[0m" % (minu, sec))
        print(info, end="")
        print("\b" * (len(info) * 2), end="", flush=True)
        time.sleep(1)
    print("\n")


while not stop_mask:
    try:
        for user_task_list in all_task_list:
            exec("start = int(" + user_task_list + "[0])")
            exec("end = int(" + user_task_list + "[1])")
            session_main(start, end)
        break
    except TypeError:
        ban_count()

