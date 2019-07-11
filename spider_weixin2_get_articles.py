import requests
import redis
import json
import re
import random
import time
import pdb

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

gzlist = ['chainnewscom']


url = 'https://mp.weixin.qq.com'
header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    }

with open('cookie.txt', 'r', encoding='utf-8') as f:
    cookie = f.read()
cookies = json.loads(cookie)
response = requests.get(url=url, cookies=cookies)
token = re.findall(r'token=(\d+)', str(response.url))[0]

article_urls = []
result = ""

# 少于50篇
count100 = 0

for query in gzlist:
    query_id = {
        'action': 'search_biz',
        'token' : token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': query,
        'begin': '0',
        'count': '5',
    }
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
    lists = search_response.json().get('list')[0]
    fakeid = lists.get('fakeid')
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
    }
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    max_num = appmsg_response.json().get('app_msg_cnt')
    num = int(int(max_num) / 5)
    begin = 0
    while num + 1 > 0 :
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        print('翻页###################',begin)
        query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
        fakeid_list = query_fakeid_response.json().get('app_msg_list')

        for item in fakeid_list:
            article_url = item.get('link')
            print(article_url)
            article_urls.append(article_url)

            article_title="wu"
            spider_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))#获取当前时间
            reporter_id = 3
            try:
               connection = mysql.connector.connect(host='localhost',
                                         database='firstcoin',
                                         user='root',
                                         password='')

               sql_insert_query = """ INSERT INTO `spider_article_urls`
                                      (`reporter_id`, `article_url`, `article_title`, `spider_time`) VALUES (%s, %s, %s, %s) """
               cursor = connection.cursor()
               result  = cursor.execute(sql_insert_query,(reporter_id, article_url, article_title, spider_time))
               connection.commit()
               print ("Record inserted successfully into python_users table")
            except mysql.connector.Error as error :
                connection.rollback() #rollback if any exception occured
                print("Failed inserting record into python_users table {}".format(error))
            finally:
                #closing database connection.
                if(connection.is_connected()):
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed")

            # with open('lanhubiji_urls.txt', 'w+', encoding='utf-8') as f:
            #     f.write(article_urls)

            count100 += 1



        num -= 1
        begin = int(begin)
        begin+=5
        time.sleep(random.randint(3, 8))

    print(count100)
    if count100>50:
        break


#
# article_urls = json.dumps(article_urls)
#
# with open('article_urls.txt', 'w+', encoding='utf-8') as f:
#     f.write(article_urls)
#
# import mysql.connector
# from mysql.connector import Error
# from mysql.connector import errorcode
# article_title="wu"
# spider_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))#获取当前时间
# reporter_id = 3
# article_urls = result.split(",")
# for article_url in article_urls:
#     try:
#        connection = mysql.connector.connect(host='localhost',
#                                  database='firstcoin',
#                                  user='root',
#                                  password='')
#
#        sql_insert_query = """ INSERT INTO `spider_article_urls`
#                               (`reporter_id`, `article_url`, `article_title`, `spider_time`) VALUES (%s, %s, %s, %s) """
#        cursor = connection.cursor()
#        result  = cursor.execute(sql_insert_query,(reporter_id, article_url, article_title, spider_time))
#        connection.commit()
#        print ("Record inserted successfully into python_users table")
#     except mysql.connector.Error as error :
#         connection.rollback() #rollback if any exception occured
#         print("Failed inserting record into python_users table {}".format(error))
#     finally:
#         #closing database connection.
#         if(connection.is_connected()):
#             cursor.close()
#             connection.close()
#             print("MySQL connection is closed")
