import requests
import pymysql
import json
import time
import random
from lxml import html
from bs4 import BeautifulSoup
import uuid
import re
import shutil

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

import pdb

with open('lanhubiji_urls.txt', 'r', encoding='utf-8') as f:
    _HEAD2 = {
        # Referer 抓取哪个网站的图片，添加此头部，可以破解盗链
        "Referer": "",
        'Accept-language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    # article_urls = f.read()
    # article_urls = json.loads(article_urls)

    # article_urls = random.sample(article_urls, 1)

    connection = mysql.connector.connect(host='localhost',
                              database='firstcoin',
                              user='root',
                              password='')

    sql_insert_query = """ SELECT * FROM `spider_article_urls` WHERE `reporter_id` = '3' """
    cursor = connection.cursor()
    result  = cursor.execute(sql_insert_query)
    result = cursor.fetchall()
    article_urls = []
    for rows in result:
        article_urls.append(rows[2])


    for article_url in article_urls:
        content=requests.get(article_url)
        body = content.content
        bs4 = BeautifulSoup(body)
        headline = bs4.find('h2', class_='rich_media_title').get_text()
        content = bs4.find("div", class_='rich_media_content').prettify().decode("utf8mb4")
        # covers = bs4.find('div', class_='rich_media_content').findAll("img")

        # 封面
        pattern = re.compile(r'var msg_cdn_url = "(.*?)"', re.MULTILINE | re.DOTALL)
        script = bs4.find("script", text=pattern)
        cover = pattern.search(script.text).group(1)
        print(cover)

        # with open('content.txt', 'w+', encoding='utf-8') as f:
        #     f.write(content)

        pattern2 = re.compile(r'var t="(.*?)",n="(.*?)",s="(.*?)"', re.MULTILINE | re.DOTALL)
        script2 = bs4.find("script", text=pattern2)
        pub_date = pattern2.search(script2.text).group(3)

        # pub_date = bs4.find("em", id_='publish_time').prettify()
        # pub_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))#获取当前时间
        reporter_id = 3

        path = "../mysite/media/articles/covers/201906/"+str(uuid.uuid1()) + '.jpg'
        r = requests.get(cover, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as cover:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, cover)
                print(cover.name)
                cover = cover.name
                cover = cover.replace('../mysite/media/','')
        pageviews = random.randint(10, 245)
        print(pageviews)
        time.sleep(random.randint(5, 8))

        import mysql.connector
        from mysql.connector import Error
        from mysql.connector import errorcode
        try:
            connection = mysql.connector.connect(host='localhost',
                                     database='firstcoin',
                                     user='root',
                                     password='')

            sql_selec_query = """ SELECT * FROM `news_article` WHERE `headline` LIKE '%s' """ % (headline)
            cursor = connection.cursor()
            cursor.execute(sql_selec_query)
            # 获取所有记录列表
            results = cursor.fetchall()
            # pdb.set_trace()

            if (len(results) == 0):
                sql_insert_query = """ INSERT INTO `news_article`
                                  (`pub_date`, `headline`, `content`, `reporter_id`, `cover`, `pageviews`) VALUES (%s, %s, %s, %s, %s, %s) """
                cursor = connection.cursor()
                result  = cursor.execute(sql_insert_query,(pub_date, headline, content, reporter_id, cover, pageviews))
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
