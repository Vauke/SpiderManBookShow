#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Filename      : spider2.py
#
# Author        : Vauke
# Create        : 2018-06-23 19:52:26
# Last Modified : 2018-06-26 18:47:50

import requests
from bs4 import BeautifulSoup
import random
import json

def get_page():
    url = 'https://book.douban.com/latest'
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
    }
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        parse_page(response.text)

def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('ul li')
    all_list = []
    cate = ['青年', '情感', '财政', '科学', '艺术', '生活', '教育', '网络']

    for i in items:
        all_list_item = {}
        if len(all_list):
            id = all_list[-1]["id"] + 1
        else:
            id = 1
        all_list_item["id"] = id

        #print('i----', i)
        pic_urls = i.select('a img')
        if len(pic_urls) != 0:
            #print('len---', pic[0])
            #图片url
            pic_url = pic_urls[0].attrs['src']
            all_list_item["pic"] = pic_url
            #print('----pic', pic_url)

            #书名
            title = i.select('h2 a')[0].string
            all_list_item["title"] = title
            #print('----title', title)

            #评分
            rating = i.select('p .font-small')[0].string.strip()
            #print('r---', rating)
            if rating == '评价人数不足' or rating == '' or rating == '目前无人评价':
                rating = '6.7'
            #rank = str(rank1).trim()
            #print('---rank', type(rank1))
            rating = float(rating)
            all_list_item["rating"] = rating
            #print('---rating', rating)
            #print('---rating', type(rating))

            all_info = i.select('.detail-frame p')
            #author = i.select('.detail-frame .color-gray')[0].string.strip()
            #作者
            author = all_info[1].string.strip()
            all_list_item["author"] = author
            #print(author)
            #简介
            info = all_info[2].string.strip()
            all_list_item["info"] = info
            #print('---info', info)

            i =  random.randint(0, 7)
            all_list_item["cate"] = cate[i]
            #print('---all', all_list_item)
            all_list.append(all_list_item)
    write2file(all_list)

def write(all_list):
    json_rst = json.dumps(all_list)
    with open('data.json', 'w+') as w:
        w.write(json_rst)

def write2file(all_list):
    for item in all_list:
        pic_url = item["pic"]
        pic = requests.get(pic_url)
        pic_name = pic_url.split('/')[-1]

        # 修改图片名, 读取本地时用
        item["pic"] = pic_name

        filename = '../uploads/'+pic_name

        with open(filename, 'wb+') as w:
            w.write(pic.content)

    write(all_list)

def main():
    get_page()

if __name__ == '__main__':
    main()
