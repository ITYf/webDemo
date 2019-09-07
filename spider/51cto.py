# -*- coding: utf-8 -*-
__author__ = 'yf'
__date__ = '2019/8/30 17:11'

from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import pymysql
import os

base_url = 'http://www.51cto.com/php/get_channel_artlist.php?'
articles = {}

headers = {
    'Host': 'www.51cto.com',
    'Referer': 'http://www.51cto.com/',
    'Cookie': 'gr_user_id=370b04b8-46b7-4ee3-949e-c2a52899b201; _ourplusFirstTime=119-7-8-13-14-51; www51cto=88AB186E823CF07D2D2B0D0089D93076ezNM; UM_distinctid=16bd00192d1135-0e47b576053d1f-e343166-144000-16bd00192d2272; yd_cookie=b26af424-2682-4879ce121c589aeec6b8709db79bda5a282d; acw_tc=b65cfd3d15672080788847906e1126870cbb03cbe37c00ee06e0c8f032582e; PHPSESSID=09311208f5513cfa46962295f228c4c5; 51ctologToken=9eac739f8fd9b4a0d79eab12546efece; pub_cookietime=0; pub_wechatnick=%E8%80%81%E9%93%81%EF%BC%8C%E6%9D%A5%E6%9D%AF%E6%8B%BF%E9%93%81; ad_2019_blogact_72home=1; gr_session_id_8c51975c40edfb67=35c2bcb5-bec5-446b-b5e7-2a3a80150508; gr_session_id_8c51975c40edfb67_35c2bcb5-bec5-446b-b5e7-2a3a80150508=true; CNZZDATA1260762011=1699404095-1562561813-null%7C1567208146; Hm_lvt_110fc9b2e1cae4d110b7959ee4f27e3b=1567163408,1567167442,1567210876,1567210929; Hm_lpvt_110fc9b2e1cae4d110b7959ee4f27e3b=1567210929; _ourplusReturnCount=10; _ourplusReturnTime=119-8-31-8-22-9; callback_api_url=https%3A%2F%2Fhome.51cto.com%2Findex%3Freback%3Dhttp%3A%2F%2Fwww.51cto.com%2F; _51ctologStr=data%3D%257Bvisitorid%3A%25229eac739f8fd9b4a0d79eab12546efece%2522%2CuserAagent%3A%2522Mozilla/5.0%2520%28Windows%2520NT%252010.0%3B%2520Win64%3B%2520x64%29%2520AppleWebKit/537.36%2520%28KHTML%2520%2520like%2520Gecko%29%2520Chrome/76.0.3809.132%2520Safari/537.36%2522%2Ctoken%3A%25229eac739f8fd9b4a0d79eab12546efece%2522%2Cuid%3A%2522%2522%2Cuuid%3A%25225559b091-106b-cf60-tdc7-o9767eb61348%2522%2Ctype%3A%2522close%2522%2Cdom%3A%2522%2522%2CdomId%3A%2522%2522%2CdomInnerTxt%3A%2522%2522%2Cprice%3A%2522%2522%2Cstudents_count%3A%2522%2522%2Cfavourite%3A%2522%2522%2Cvote%3A%2522%2522%2Cscrolling%3A%25220%2525%2522%2Cscreensize%3A%25221536X864%2522%2Curl%3A%2522https%25253A%25252F%25252Fhome.51cto.com%25252Findex%25253Freback%25253Dhttp%25253A%25252F%25252Fwww.51cto.com%25252F%2522%2Cref%3A%2522http%25253A%25252F%25252Fwww.51cto.com%25252F%2522%2Cfrom%3A%2522home%2522%2Cduration%3A%252217463%2522%2Ctime%3A%25221567210960252%2522%257D; pub_sauth1=FhwMAFNcVQMABQdSAQFXPQUHAVVTAAIFa1ICUgJWUwRYUgo; pub_sauth2=809b09400f6335c20cbce312359f8815; pub_wechatopen=DgZDExYRD1R3AXpSFnsTc2V1f1xSQG1iDRpmNTwLMWwlN0oXKxZnC1ByRF4tfVBjcn1nUi4Cb19SakAcBlRRBwcBDVBdVVQBUVELCWoIUwIDAQVUXwQG; pub_sauth3=BABcAlJYUAMHAANTVlRUBlBVAF5bAwAEUFAFDABUV1ZVBw4HX19SBWxaVQBWBQdRB1VVClBVVAwNBAMMXV0HVVUIDVVeAABRVQcEA1ZWVQYGPlcNVVZQBAFUAAo',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_html(id, page):
    params = {
        'id': id,
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def get_detail(url):
    try:
        response = requests.get(url)
        response.encoding = 'gbk'
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_page(list):
    if list:
        # 每发起一次Ajax请求，会请求到一个包含30篇文章详细信息的列表，类型为：list
        items = list[0]
        # 获取每一篇文章的详细信息item，类型为：dict

        for item in items:
            articles['title'] = item.get('title').replace('?','').replace('/','')
            articles['keywords'] = pq(item.get('keywords')).text()
            articles['pub_time'] = item.get('stime')
            articles['img_url'] = item.get('picname')
            articles['url'] = item.get('url')
            # articles['content']=get_detail(url)
            yield articles


def save_img(item, id):
    # 判断当前目录是否有此名的文件夹。没有就创建。也避免了重复创建
    if not os.path.exists('id=' + str(id)):
        os.mkdir('id=' + str(id))
    try:
        # 根据图片链接，请求到图片的二进制数据
        response = requests.get(item.get('img_url'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format('id=' + str(id), item.get('title'), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')


def delete_query():
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='news')
    cursor = db.cursor()
    table = 'articles_id_15'
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
    table = 'articles_id_15'
    keys = ','.join(data.keys())
    values = ','.join(['%s'] * len(data))  # 构造一个 %s 的占位符序列，个数就是传入数据的长度
    add_query(db, data, keys, values, table)  # 调用 add_db 方法


if __name__ == '__main__':
    # delete_query()
    '''上次爬取完第27页'''
    for page in range(18,50):
        id = 15
        list = get_html(id, page)
        results = parse_page(list)
        print('第%s页爬取完成' % page)
        for result in results:
            save_img(result, id)
            save_info(result)

