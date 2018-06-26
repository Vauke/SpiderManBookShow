#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Filename      : views.py
#
# Author        : Vauke
# Create        : 2018-06-24 21:16:50
# Last Modified : 2018-06-27 00:47:42

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
import os
import re
from . import settings

flag = False
uploads = settings.STATICFILES_DIRS[-1][-1]
b_id = -1

def read_json():
    with open('/media/Program/Python_Projects/test/gcxj/bookshow/bookshow/data.json', 'r+') as r:
        rst = r.read()
    if len(rst):
        book_list = json.loads(rst)
    return book_list

def write_json(book_list):
    rst = json.dumps(book_list)
    with open('/media/Program/Python_Projects/test/gcxj/bookshow/bookshow/data.json', 'w+') as w:
        w.write(rst)

def write_pic(pic):
    # 获取要上传到的路径
    global uploads

    # 如果路径不存在则新建
    if not os.path.isdir(uploads):
        os.mkdir(uploads)
    else:
        filename = '%s/%s'%(uploads, pic.name)

    # 写入文件, 必须使用chunks(), 因为文件上传采用块上传
    with open(filename, 'wb+') as wb:
        for chunk in pic.chunks():
            wb.write(chunk)

def index(request):
    context = {}
    context['book_list'] = read_json()
    return render(request, 'index.html', context)

def rating_sort(request):
    context = {}
    global flag
    if flag:
        flag = False
    else:
        flag = True
    book_list = read_json()
    book_list = sorted(book_list, key = lambda x:x['rating'], reverse = flag)
    context['book_list'] = book_list
    return render(request, 'index.html', context)

def del_book(request):
    context = {}
    book_list = read_json()
    book_id = request.GET['book_id']
    #print('type----', type(id))

    global uploads

    for i in book_list:
        if i['id'] == eval(book_id):
            book_list.remove(i)
            filename = '%s/%s'%(uploads, i['pic'])
            #print('---filename', filename)
            # 如果不是目录, 删除对应文件
            if not os.path.isdir(filename):
                os.remove(filename)

    write_json(book_list)

    #filename = '%s/%s'%(uploads, pic.name)
    context['book_list'] = book_list
    return render(request, 'index.html', context)

def cate(request):
    context = {}
    condition = request.GET['condition']
    book_list = read_json()
    condition_list = []
    for i in book_list:
        if i['cate'] == condition:
            condition_list.append(i)
    context['condition_list'] = condition_list
    return render(request, 'category.html', context)

def add_book(request):
    return render(request, 'add_book.html')

def add_done(request):
    context = {}
    book_list = read_json()
    book = {}

    # 使用request.FILES.get()来获取上传的文件
    pic = request.FILES.get('pic')
    #pic = request.POST['pic']
    title = request.POST['title']
    author = request.POST['author']
    rating = request.POST['rating']
    info = request.POST['info']
    cate = request.POST['cate']

    write_pic(pic)
#    if not os.path.isdir(uploads):
#        os.mkdir(uploads)
#    else:
#        #print('---------')
#        filename = '%s/%s'%(uploads, pic.name)
#    with open(filename, 'wb+') as wb:
#        for chunk in pic.chunks():
#            wb.write(chunk)
#        
#    #print(uploads)

    if len(book_list):
        book_id = book_list[-1]['id'] + 1
    else:
        book_id = 1

    book['id'] = book_id
    book['pic'] = pic.name
    book['title'] = title
    book['rating'] = rating
    book['author'] = author
    book['info'] = info
    book['cate'] = cate
    book_list.append(book)

    #print('---book', book)
    write_json(book_list)

    context['book_list'] = book_list
    return render(request, 'index.html', context)

def edit_book(request):
    global b_id

    b_id = request.GET['book_id']
    return render(request, 'edit_book.html')

def edit_done(request):
    context = {}
    book_list = read_json()
    title = request.POST['title']
    author = request.POST['author']
    info = request.POST['info']

    global b_id
    #print('---b_id', b_id)

    if b_id:
        for i in book_list:
            if i['id'] == eval(b_id):
                i['title'] = title
                i['author'] = author
                i['info'] = info
                # print('---i', i)
                write_json(book_list)
    context['book_list'] = book_list
    return render(request, 'index.html', context)

def search_book(request):
    context = {}
    title = request.POST['title']
    #print('---title', type(title))
    book_list = read_json()
    search_rst = []

    for i in book_list:
        info = re.findall(r'.*?'+'%s.*?'%title, i['title'])
        #print(info)
        #print('.*?'+title+'.*?')
        #if i['title'] == title:
        if len(info):
            search_rst.append(i)

    context['search_rst'] = search_rst
    return render(request, 'search.html', context)
