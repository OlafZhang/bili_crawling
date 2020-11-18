# bili_crawing

爬取b站用户信息

从2020.7开始，截至至2020.11.18，已经爬取250,0000+条数据，现停止此项目

## 简单说明

仅支持Python3

main.py只有一个地方需要改：IFTTT配置。将其更改为自己的IFTTT配置，或者弃用

IFTTT模块通过def的形式存在，方法名为```send_notice_ifttt(text1, text2)```

main.py的其它配置均在runtime.cfg可以配置

其它py文件需要修改内部的相关代码和参数，如mysql密码

## 程序

| 程序 | 解释 | 备注 |
| :---:| :---: | :---: |
| main.py | 主程序 | 配置文件为runtime.cfg |
| check_mysql.py | 随机抽查数据库，以确定某个区间数据是否完整 |  |
| side.py | 二次爬取程序 | 从数据库检查缺失数据并爬取，但写入到一个sql文件 |
| sql_import.py | 数据库区间导入 |  |
| sql_output.py | 数据库区间导出 |  |

## 数据库

使用MySQL作为数据库，数据库名称为bili,表名称为bili_user,数据库文件为bili_user_20201118.7z(其中有csv文件)

表结构：

| 名字 | 说明 | 类型 | 长度 | 小数点 | 非null | 主键 | 备注 | 
| :---:| :---: | :---: | :---: | :---: | :---: |:---: |:---: |
| UID | 用户的UID | decimal | 9 | 0 | 是 | 是 | |
| NAME | 用户名 | text | 0 | 0 | 否 | 否 | |
| FOLLOWER | 粉丝数量 | decimal | 9 | 0 | 否 | 否 | |
| FOLLOWING | 关注量 | decimal | 9 | 0 | 否 | 否 | |
| 100_UP | 是否是(或曾经是)百大UP | tinyint | 1 | 0 | 是 | 否 | 默认值为0 |

如今的bilib已经具备爬取性别，等级等更多信息的能力，但开发出bilib时已经船大难掉头

## 外部调用

需要调用[bilib](https://github.com/OlafZhang/bilib)

截止至2020.11.18，bilib仍然对此项目有效

开启带颜色字模式需要colorama，否则会报错

进度条需要tqdm支持

数据库写入需要pymysql支持

其它请参考bilib的requirement.txt

## 测试

在CentOS 8.0，Ubuntu Server 20.04, iPad OS(运行Pythonista)经过简单修改配置文件稳定运行

在Windows 10可能会导致系统卡死(至少我的电脑会)

## 备注

此代码算是被我封存了，但是欢迎各位继续研究