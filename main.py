# 导入库
import sys
from tqdm import tqdm

# 读取配置文件
try:
    print("[*]Loading runtime.cfg...")
    config = open("runtime.cfg", "r", encoding="utf-8")
    all_task_list = []
    for i in config.readlines():
        if i[0] == "#" or i[0] == "" or i[0] == " " or i[0] == "\n":
            pass
        else:
            if i[0:5] == "task_":
                name = str(i).split(" = ")[0]
                all_task_list.append(name)
            else:
                pass
            exec(i)
            i = i[0:len(i) - 1]
            if len(i) != 0:
                print(("[*]%s") % (i))
            else:
                pass
    config.close()
    print("[*]Loaded all values in runtime.cfg")
except Exception:
    print("[!]Something wrong with your config files!")
    print("[!]Or you did not have runtime.cfg!")
    print("[!]Quiting!")
    sys.exit(1)

if disable_color == True:
    pass
else:
    try:
        from colorama import init
    except:
        print("Install colorama, then retry.")
        sys.exit(1)

import bilib
bilib.set_timeout(10)

# println为真时在单行刷新
def color_print(string, color="yellow", println=False):
    string = str(string)
    if disable_color:
        print(string)
    else:
        if println:
            end = ""
        else:
            end = "\n"
        if color == str("cyan"):
            print("\033[1;36m%s\033[0m" % string, end=end)
        elif color == str("blue"):
            print("\033[1;34m%s\033[0m" % string, end=end)
        elif color == str("pink"):
            print("\033[1;35m%s\033[0m" % string, end=end)
        elif color == str("green"):
            print("\033[1;32m%s\033[0m" % string, end=end)
        elif color == str("red"):
            print("\033[1;31m%s\033[0m" % string, end=end)
        elif color == str("yellow"):
            print("\033[1;33m%s\033[0m" % string, end=end)
        else:
            print("\033[1;33m%s\033[0m" % string, end=end)
        if println:
            print("\b" * (len(string) * 2), end="", flush=True)
        else:
            pass

color_print("[*]Loading Main Session...")

need_import = ['os', 'platform', 'requests', 'time', 'datetime', 'traceback', 'random', 'json', 'fake_useragent',
               'datetime']

# 以下为初始化的数值，勿动
stop_mask = False
connect_ok = True
user_id_pick = "NULL"
runtime_task_session = 0

for i in need_import:
    try:
        loading_info = str("[*]Import %s" % i)
        color_print(loading_info, println=True)
        exec("import %s" % i)
        loaded_info = str("[*]Import %s OK!" % i)
        color_print(loaded_info, color="green")
    except ModuleNotFoundError:
        fail_info = str("[!]%s is not installed, installing..." % i)
        color_print(fail_info, color="red")
        sysstr = platform.system()
        if sysstr == "Windows":
            os.system("pip install " + str(i))
        else:
            os.system("pip3 install " + str(i))
        exec("import %s" % i)
        loaded_info = str("[*]Import %s OK!" % i)
        color_print(loaded_info, color="green")

# 判断系统
sysstr = platform.system()
if sysstr == "Windows":
    color_print("[*]A Windows machine")
    linux = False
elif sysstr == "Linux":
    color_print("[*]A Linux/Android machine")
    os.system("free -h")
    os.system("neofetch")
    time.sleep(1)
    linux = True
elif sysstr == "Darwin":
    color_print("[*]A macOS/iOS machine")
    time.sleep(1)
    linux = True
else:
    color_print("[!]Undefined machine:%s" % sysstr, color="red")
    color_print("[*]As a Linux machine")
    linux = True

# 初始化IFTTT
def send_notice_ifttt(text1, text2):
    info = str(("来自 %s:%s") % (text1, text2))
    time_out = 3
    if ifttt_debug:
        color_print("[*]IFTTT debuging(%s)" % info, color="red")
    else:
        color_print("[*]Send Message via IFTTT...(%s)" % info, color="green")
        url = f"https://maker.ifttt.com/trigger/python3_crawlsql_notice/with/key/ijVxLn62cIj7mDNcMvBsbTyIAm758xJ5eMP6X8H6rA4"
        payload = {"value1": text1, "value2": text2}
        headers = {"Content-Type": "application/json"}
        while True:
            try:
                response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
                if str(response.text)[0:15] == 'Congratulations':
                    color_print("[*]Send Done.", color="green")
                    break
                else:
                    color_print("[!]Resending...", color="red")
            except requests.exceptions.ConnectionError:
                if time_out != 0:
                    color_print("[!]Resending after 10s...", color="red")
                    time.sleep(10)
                    time_out -= 1
                    continue
                else:
                    color_print("[!]Seems IFTTT blocking, now output message...", color="red")
                    color_print("[*]%s" % info, color="green")
                    break

color_print("[*]Loaded IFTTT.", color="green")
if ifttt_debug:
    send_notice_ifttt(device, "爬取程序已启动。")
else:
    ifttt_debug = True
    send_notice_ifttt(device, "爬取程序已启动。")
    ifttt_debug = False

# 连接数据库
if no_sql:
    color_print("[*]No SQL, use file output.")
else:
    import pymysql

    color_print("[*]Connecting MySQL...")
    try:
        db = pymysql.connect(sql_ip, sql_user, sql_pass, sql_database)
        color_print("[*]MySQL OK.")
    except pymysql.err.OperationalError:
        color_print("[-]Wrong Username/Password/MySQL_Host, check source code, quiting...", color="red")
        time.sleep(3)
        sys.exit(1)
color_print("[!] -----------------------------------------------------------", color="yellow")
color_print("[+]  ___  _        _    _____   ______   _    _    _   _  ____ ", color="red")
color_print("[-] / _ \| |      / \  |  ___| |__  / | | |  / \  | \ | |/ ___|", color="pink")
color_print("[\]| | | | |     / _ \ | |_      / /| |_| | / _ \ |  \| | |  _ ", color="blue")
color_print("[|]| |_| | |___ / ___ \|  _|    / /_|  _  |/ ___ \| |\  | |_| |", color="cyan")
color_print("[/] \___/|_____/_/   \_\_|     /____|_| |_/_/   \_\_| \_|\____|", color="green")
color_print("[?] -----------------------------------------------------------", color="yellow")
if disable_color:
    print("Powered by Olaf Zhang.All right reserved.")
else:
    color_list = ["yellow","red","pink","blue","cyan","green"]
    for zhuang_b_time in range(0,10):
        for color in color_list:
            time.sleep(0.01)
            color_print("Powered by Olaf Zhang.All right reserved.", color=color ,println=True)
    print("\n")
color_print("[*]List tasks.", color="cyan")
main_task = 0
all_total = 0
for user_task_list in all_task_list:
    exec("start = int(" + user_task_list + "[0])")
    exec("end = int(" + user_task_list + "[1])")
    total = end - start + 1
    all_total += total
    list_name = user_task_list
    main_task += 1
    color_print('[+]Found list %s: Call "%s", from %s to %s, total %s.' % (main_task, list_name, start, end, total),
                color="green")
color_print("[*]List tasks OK, total:%s" % all_total, color="cyan")
color_print("[*]SleepTime from %s secs to %s secs." % (sleep_start / 10, sleep_end / 10), color="cyan")

# 构建主程序
color_print("[*]Buliding def...")

def session_main(start, end):
    color_print("[*]Range from %s to %s" % (str(start), str(end)))
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
    for user_task_list in all_task_list:
        exec("global " + user_task_list)
    task_session = 1
    list_uid = []
    color_print("[*]Creating list.")
    for i in range(int(start), int(end) + 1):
        list_uid.append(int(i))
    for i in range(0, 10):
        random.shuffle(list_uid)
    if no_sql:
        if linux:
            home_dir = str(os.path.abspath('.') + "/")
        else:
            home_dir = str(os.path.abspath('.') + "\\")
        file_name = str("mysql_from_%s_to_%s.sql" % (str(start), str(end)))
        sql = str(home_dir + file_name)
        if os.path.exists(sql):
            color_print("[*]File existed, now loading...")
            pass
        else:
            import pathlib
            pathlib.Path(sql).touch()
            color_print("[+]File touched.", color="cyan")
        mask_no = 0
        mask = ["-", "/", "|", "\\"]
        start_sec = datetime.datetime.now()
        total_readline = len(open(sql, 'r', encoding="utf-8").readlines())
        sql_file = open(sql, 'r', encoding='utf-8')
        with tqdm(total=total_readline, desc="Loading") as pbar:
            for line in sql_file.readlines():
                text = str(line)  # 转换当前行为字符串
                text = text.split('values(')  # 切面包：分割
                text = str(text[1])  # 挑出含UID的列表元素
                text = text.split(',')  # 切面包：分割
                text = str(text[0])
                if int(text) in list_uid:  # 如果sql文件的UID已经在列表里了，在UID列表删除此UID
                    list_uid.remove(int(text))
                    task_session += 1  # 进程号+1
                else:
                    pass
                pbar.update(1)
        end_sec = datetime.datetime.now()
        used_time = str((end_sec - start_sec).seconds)
        color_print("[*]Initialization completed:%s, used %s secs." % (task_session, used_time), color="green")
        print("\n")
        task_session += 1
        sql_file.close()
    else:
        pass
    color_print("[*]---START-TASKS---", color="pink")
    for id in list_uid:
        try:
            global user_id_pick
            user_id_pick = id
            time_now = str(time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime()))
            start_info = str("[*]At " + time_now + " choice " + str(id) + ".")
            color_print(start_info)
            if no_sql:
                data_exist = 0
            else:
                find_uid = db.cursor()
                data_exist = find_uid.execute("select * from bili_user where UID = " + str(id))

            if data_exist == 0:
                ua_list = fake_useragent.UserAgent()
                color_print("[+]Generate fake UA.", color="cyan", println=True)
                ua = ua_list.random
                color_print("[*]User Agent:%s" % ua, color="green")
                headers = {"User-Agent": str(ua)}
                get_info_status = False
                get_info_fail = False
                try:
                    color_print("[*]Get info from APIs...", println=True)
                    get_time = 1
                    while True:
                        try:
                            full_info = bilib.user_info(id)
                            following = full_info['following']
                            fans = full_info['fans']
                            raw_name = full_info["name"]
                            sex = str(full_info["sex"])
                            level = str(full_info["level"])
                            face_url = str(full_info["face_url"])
                            coins = str(full_info["coins"])
                            sign = str(full_info["sign"])
                            birthday = str(full_info["birthday"])
                            vip_type = str(full_info["vip_type"])
                            name = str("")
                            for i in range(0, len(raw_name)):
                                if raw_name[i] == str("\\"):
                                    name += "\\"
                                elif raw_name[i] == str("\{"):
                                    name += "\{"
                                elif raw_name[i] == str("\}"):
                                    name += "\}"
                                else:
                                    name += raw_name[i]
                            get_info_status = True
                            get_time += 1
                            color_print("[*]Get info from APIs...OK       ", color="green")
                            break
                        except bilib.Timeout:
                            if int(get_time) == 4:
                                color_print('[-]Network maybe bad,now skip...', color="red")
                                list_uid.remove(int(id))
                                list_uid.append(int(id))
                                get_info_fail = True
                                color_print("[*]----END-A-TASK----", color="pink")
                                break
                            else:
                                color_print(str('[-]Timeout,retry...' + str(get_time) + "                          "), color="red", println=True)
                                get_time += 1
                                continue
                except bilib.SeemsNothing:
                    get_info_status = True
                    name = str("(##不存在用户##)")
                    fans = 0
                    following = 0
                    sex = str("(##NONE##)")
                    level = str("0")
                    face_url = str("(##NONE##)")
                    coins = str("0")
                    sign = str("(##NONE##)")
                    birthday = str("(##NONE##)")
                    vip_type = str("(##NONE##)")
                except bilib.RequestError:
                    color_print("[!]Request Error                         ", color="red")
                except bilib.RequestRefuse:
                    color_print("[!]Request Refuse                          ", color="red")
                    ban_count()
                if not get_info_status:
                    list_uid.remove(int(id))
                    list_uid.append(int(id))
                    continue
                else:
                    color_print(
                        str("[+]Task_" + str(task_session) + ":" + str(id) + "(" + str(name) + ") with " + str(
                            fans) + " fan(s) and " + str(following) + " following(s)."), color="cyan")
                    if get_info_status:
                        color_print(str("[+]Sex: " + sex), color="cyan")
                        color_print(str("[+]Level: " + level), color="cyan")
                        color_print(str("[+]Face URL: " + face_url), color="cyan")
                        color_print(str("[+]Coins: " + coins), color="cyan")
                        if len(sign) == 0:
                            sign = str("(##NONE##)")
                        else:
                            sign = str(full_info["sign"])
                        color_print(str("[+]Sign: " + sign), color="cyan")

                        if len(birthday) == 0:
                            birthday = str("(##NONE##)")
                        else:
                            birthday = str(full_info["birthday"])
                        color_print(str("[+]Birthday: " + birthday), color="cyan")

                        if len(vip_type) == 0:
                            vip_type = str("(##NONE##)")
                        else:
                            vip_type = str(full_info["vip_type"])
                        color_print(str("[+]VIP type: " + vip_type), color="cyan")
                    else:
                        pass

                    into_command = str(
                        "insert into bili_user values(" + str(id) + ",'" + str(name) + "'," + str(fans) + "," + str(
                            following) + ",0)")
                    if no_sql:
                        sql_file = open(sql, 'a', encoding='utf-8')
                        sql_file.write(into_command + ";\n")
                        sql_file.close()
                    else:
                        try:
                            cursor = db.cursor()
                            cursor.execute(into_command)
                            color_print("[*]Command:%s" % into_command)
                            db.commit()
                        except Exception:
                            db.rollback()
                    sleep_time = random.randint(sleep_start, sleep_end)
                    sleep_time = sleep_time / 10
                    color_print(str("[*]Sleep time " + str(sleep_time) + " sec."))
                    time.sleep(sleep_time)
            else:
                color_print("[*]Task_%s:%s existed ,skipping." % (task_session, user_id_pick))
            color_print("[*]----END-A-TASK----", color="pink")
            if get_info_fail:
                pass
            else:
                runtime_task_session += 1
                task_session += 1
                retry_time = 10

        except KeyboardInterrupt:
            if no_sql:
                try:
                    print(" ")
                    color_print("[!]Keyboard Interrupt detected, now pause.", color="red")
                    color_print("[*]Enter [E]xit or just Enter...", color="cyan")
                    user_input = str(input("INPUT_HERE> "))
                    if user_input == str("e") or user_input == str("E") or user_input == str(
                            "Exit") or user_input == str("exit"):
                        color_print("[!]Exit by user.", color="red")
                        sys.exit(1)
                        break
                    else:
                        pass
                except KeyboardInterrupt:
                    print(" ")
                    color_print("[!]Force exit by user.", color="red")
                    if linux:
                        pass
                    else:
                        time.sleep(3)
                    sys.exit(1)
                    break
            else:
                print(" ")
                color_print("[!]Force exit by user.", color="red")
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
                    color_print(str("[-]Check your connection, retry time:" + str(retry_time)), color="red")
                    time.sleep(10)
                    color_print("[*]Try continue...")
                    pass
                else:
                    color_print("[-]Quiting...", color="red")
                    sys.exit(1)
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
            info = str("[-]Banding now, change IP or Waiting ,ETA: %dmin %dsec." % (minu, sec))
        else:
            change = True
            info = str("[*]Banding now, change IP or Waiting ,ETA: %dmin %dsec." % (minu, sec))
        color_print(info, color="red", println=True)
        time.sleep(1)
    print("\n")

def ending_info():
    used_time = int((end_sec - start_sec).seconds)
    day = used_time // 86400
    temp_time_1 = used_time % 86400
    hour = temp_time_1 // 3600
    temp_time_2 = temp_time_1 % 3600
    minu = temp_time_2 // 60
    sec = temp_time_2 % 60
    task_session = runtime_task_session
    if task_session != 0:
        speed = int(int(used_time) // int(task_session))
        if speed == 0:
            speed = int(int(task_session) // int(used_time))
            speed_info = str(("每秒%s条") % (speed))
        else:
            speed_info = str(("每条%s秒") % (speed))
    else:
        speed_info = str(("速度信息不可用"))

    time_dynamic_info = str("")

    if day == 0:
        pass
    else:
        time_dynamic_info += str(("%s%s") % (str(day), str("天")))
    if hour == 0:
        pass
    else:
        time_dynamic_info += str(("%s%s") % (str(hour), str("小时")))
    if minu == 0:
        pass
    else:
        time_dynamic_info += str(("%s%s") % (str(minu), str("分钟")))
    if sec == 0:
        pass
    else:
        time_dynamic_info += str(("%s%s") % (str(sec), str("秒")))
    if len(time_dynamic_info) == 0:
        time_dynamic_info = str("0秒")

    final_info = str(
        ("在%s完成%s个条目(任务列表:从%s到%s)的爬取作业，%s。") % (time_dynamic_info, task_session - 1, start, end, speed_info))
    send_notice_ifttt(device, final_info)

while not stop_mask:
    try:
        for user_task_list in all_task_list:
            start_sec = datetime.datetime.now()
            exec("start = int(" + user_task_list + "[0])")
            exec("end = int(" + user_task_list + "[1])")
            session_main(start, end)
            end_sec = datetime.datetime.now()
            ending_info()
        color_print("[*]Crawling completed.")
        break
    except Exception as e:
        import time, traceback
        time_now = str(time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime()))
        color_print(str("[-]An unexpected error occured.(" + str(e) + ")"), color="red")
        color_print(str("[-]Time:%s" % time_now), color="red")
        try:
            color_print(str("[-]User ID:%s." % user_id_pick), color="red")
        except:
            color_print(str("[-]User ID:##NOT_START##."), color="red")
        traceback.print_exc()
        error_info = str("发生未预料错误(" + str(e) + ")，程序停止。")
        send_notice_ifttt(device, error_info)
        sys.exit(1)
