# -*- coding: utf-8 -*-
__author__ = 'yf'
__date__ = '2019/8/31 12:34'

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # 显示等待
import pymysql
import requests

browser = webdriver.Chrome()
browser.get('https://www.toutiao.com')
# 实例化一个 WebDriverWait 对象，指定最长等待时间
wait = WebDriverWait(browser, 8)

# 构造一个空字典
rewen = {}

'''
这里，只需要爬取前十条就行，然后再根据评论数排名过滤出来，填充到24小时热文。爬去字段：title、category、comment、url
注意： 使用 elements
'''


def get_detail(url):
    try:
        response = requests.get(url)
        response.encoding = 'gbk'
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_info():
    wait.until(lambda driver: driver.find_elements_by_css_selector(".feed-infinite-wrapper ul li"))
    toutiao_list = browser.find_elements_by_css_selector('.feed-infinite-wrapper ul li')

    for toutiao in toutiao_list[:10]:
        rewen['title'] = toutiao.find_element_by_css_selector('div .title-box a').text
        rewen['source'] = toutiao.find_element_by_css_selector(
            'div .bui-box .bui-left .footer-bar-action.source').text
        try:
            comment_num = toutiao.find_element_by_partial_link_text('评论').text
            if comment_num in '万':
                rewen['comment'] = int(comment_num[:-5]) * 10000
            else:
                rewen['comment'] = int(comment_num[:-4])
        except:
            rewen['comment'] = 0
        url = toutiao.find_element_by_css_selector('div .title-box a').get_attribute('href')
        rewen['url']=url
        rewen['content'] = get_detail(url)
        yield rewen


'''
把插入记录的操作封装到 add_db() 中，
只需要在 save_info()中修改data就行
'''


def delete_query():
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='news')
    cursor = db.cursor()
    table = 'articles_rewen'
    sql1 = 'SELECT * FROM {table}'.format(table=table)
    sql2 = 'TRUNCATE TABLE {table}'.format(table=table)
    cursor.execute(sql1)
    if cursor.rowcount != 0:
        try:
            cursor.execute(sql2)
            db.commit()
            print('已删除原有数据！')
        except:
            db.rollback()
        db.close()


def add_query(db, data, keys, values, table):
    sql = 'INSERT INTO {table}({keys}) VALUE({values})'.format(table=table, keys=keys, values=values)
    cursor = db.cursor()
    try:
        if cursor.execute(sql, tuple(data.values())):
            db.commit()
    except pymysql.MySQLError as e:
        print(e.args)
        db.rollback()
    db.close()


def save_info(data):
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='news')
    table = 'articles_rewen'
    keys = ','.join(data.keys())
    values = ','.join(['%s'] * len(data))  # 构造一个 %s 的占位符序列，个数就是传入数据的长度
    add_query(db, data, keys, values, table)  # 调用 add_db 方法


if __name__ == "__main__":
    results = get_info()
    # delete_query()
    for result in results:
        print(result)
        # save_info(result)
    print('已存储到数据库！')
    sleep(5)
    browser.close()
