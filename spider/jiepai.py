# -*- coding: utf-8 -*-
__author__ = 'yf'
__date__ = '2019/9/2 19:10'

import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool

base_url = 'https://www.toutiao.com/api/search/content/?'

imgs = {}
img = {}


def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'count': '20',
    }
    url = base_url + urlencode(params)
    print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def parse_images(json):
    # print(json.get('data'))
    if json.get('data'):
        for item in json.get('data'):
            if item.get('title') != None:
                title = item.get('title')
                if item.get('image_list') != None:
                    images = item.get('image_list')
                    for image in images:
                        yield {
                            'image_url': image.get('url'),
                            'title': title
                        }


def save_image(item):
    # 判断当前目录是否又此 title 为名的文件夹。没有就创建。也避免了重复创建
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        # 根据图片链接，请求到图片的二进制数据
        response = requests.get(item.get('image_url'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')


def main(offset):
    json = get_page(offset)
    results = parse_images(json)
    for result in results:
        save_image(result)


if __name__ == '__main__':
    pool = Pool()
    offsets = (x for x in range(0, 140, 10))
    pool.map(main, offsets)
    pool.close()
    pool.join()
