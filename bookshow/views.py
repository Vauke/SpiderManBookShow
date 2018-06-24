#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Filename      : views.py
#
# Author        : Vauke
# Create        : 2018-06-24 21:16:50
# Last Modified : 2018-06-24 21:19:13

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json

def index(request):
    context = {}
    return render(request, 'index.html', context)
