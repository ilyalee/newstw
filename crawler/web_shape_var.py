#!/usr/bin/env python
# -*- coding: utf-8 -*-

context = {}
skip = {}
source = {}
trimtext = {}

source_default = 'any'
source['chinatimes'] = ["www.chinatimes.com"]
source['ltn'] = ["www.ltn.com.tw/news", "news.ltn.com.tw"]
source['appledaily'] = ["www.appledaily.com.tw"]
source['udn'] = ["udn.com/news"]
source['pts'] = ["news.pts.org.tw"]
source['ftv'] = ["news.ftv.com.tw"]
source['setn'] = ["www.setn.com"]
source['eranews'] = ["eranews.eracom.com.tw"]
source['tvbs'] = ["news.tvbs.com.tw"]
source['ctitv'] = ["gotv.ctitv.com.tw"]
source['ettoday'] = ["www.ettoday.net"]
source['ebc'] = ["news.ebc.net.tw"]

context['any'] = [
    {'save': "title", 'path': "h1", 'ind': 0},
    {'save': "summary", 'path': "", 'ind': 0},
    {'save': "_rawtime", 'path': "time", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY-MM-DD HH:mm:ss"}
]
context['chinatimes'] = [
    {'save': "title", 'path': "header > h1", 'ind': 0},
    {'save': "summary", 'path': "article", 'ind': 1},
    {'save': "_rawtime", 'path': "time", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY年MM月DD日 HH:mm"}
]
context['ltn'] = [
    {'save': "title", 'path': "h1", 'ind': 0},
    {'save': "summary", 'path': "#newstext > p", 'ind': -1},
    {'save': "_rawtime", 'path': "#newstext > span", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': ["YYYY-MM-DD  HH:mm", "YYYY-MM-DD"]}
]
context['appledaily'] = [
    {'save': "title", 'path': "header > hgroup > h1", 'ind': 0},
    {'save': "summary", 'path': "#summary", 'ind': 0},
    {'save': "_rawtime", 'path': "time", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY年MM月DD日HH:mm"}
]
context['udn'] = [
    {'save': "title", 'path': "#story_body_content > h1", 'ind': 0},
    {'save': "summary", 'path': "#story_body_content > p", 'ind': -1},
    {'save': "_rawtime", 'path': ".story_bady_info_author", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY-MM-DD HH:mm"}
]
context['pts'] = [
    {'save': "title", 'path': "h1.article-title", 'ind': 0},
    {'save': "summary", 'path': ".article-content", 'ind': 0},
    {'save': "_rawtime", 'path': ".list-news-time", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY-MM-DD"}
]
context['ftv'] = [
    {'save': "title", 'path': "#h1 > span", 'ind': 0},
    {'save': "summary", 'path': "#newscontent", 'ind': 0},
    {'save': "_rawtime", 'path': "span#h2 > .ndate > span", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY/M/DD HH:mm"}
]
context['setn'] = [
    {'save': "title", 'path': "h1", 'ind': 0},
    {'save': "summary", 'path': "article", 'ind': 0},
    {'save': "_rawtime", 'path': [".titleBtnBlock > .title-left-area > .date", ".titleBtnBlock > .time"], 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY/MM/DD HH:mm:ss"}
]
context['eranews'] = [
    {'save': "title", 'path': "#LT_1_1", 'ind': 0},
    {'save': "summary", 'path': "#LT_1_3_1", 'ind': 0},
    {'save': "_rawtime", 'soup': 'findAll', 'path': 'text', 'ind': 4},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY/MM/DD"}
]
context['tvbs'] = [
    {'save': "title", 'path': "p.titel26 > strong", 'ind': 0},
    {'save': "summary", 'path': "div.newsdetail-content", 'ind': 0},
    {'save': "_rawtime", 'path': 'p.under15', 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY/MM/DD HH:mm"}
]
context['ctitv'] = [
    {'save': "title", 'path': "header > h1.entry-title", 'ind': 0},
    {'save': "summary", 'path': ".td-post-content > p", 'ind': -1},
    {'save': "_rawtime", 'soup': "attrs", 'path': {'time': "datetime"}, 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY-MM-DD"}
]
context['ettoday'] = [
    {'save': "title", 'path': "h2", 'ind': 0},
    {'save': "summary", 'path': "section > p", 'ind': -1},
    {'save': "_rawtime", 'path': ".news-time", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY年MM月DD日 HH:mm"}
]
context['ebc'] = [
    {'save': "title", 'path': ".newsTargetTitle > h1", 'ind': 0},
    {'save': "summary", 'path': "#contentBody", 'ind': 0},
    {'save': "_rawtime", 'path': ".ml15.mt10", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY-MM-DD HH:mm"}
]

skip['any'] = []
skip['chinatimes'] = ['figure']
skip['udn'] = ['figure']

trimtext['any'] = []
trimtext['ltn'] = ['相關影音']
trimtext['ctitv'] = ['※中天快點TV非讀不可:']
trimtext['udn'] = ['分享facebook']
