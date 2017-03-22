#!/usr/bin/env python
# -*- coding: utf-8 -*-

context = {}
skip = {}
source = {}
trimtext = {}

source_default = 'any'
source['chinatimes'] = ["www.chinatimes.com"]
source['ltn'] = [
    "www.ltn.com.tw/news",
    "news.ltn.com.tw"
]
source['appledaily'] = ["www.appledaily.com.tw"]
source['udn'] = ["udn.com"]
source['pts'] = [
    "news.pts.org.tw",
    "about.pts.org.tw/rss/XML/newsfeed.xml",
    "UCexpzYDEnfmAvPSfG4xbcjA"
]
source['ftv'] = [
    "news.ftv.com.tw",
    "04784784225885481651/2830296333612041371",
    "UC2VmWn8dAqkzlQqvy02E1PA"
]
source['setn'] = [
    "www.setn.com",
    "04784784225885481651/2327852074443664022",
    "UCIU8ha-NHmLjtUwU7dFiXUA"
]
source['eranews'] = [
    "eranews.eracom.com.tw",
    "UCHBv5vSp3pETSLq8oWTsmqA"
]
source['tvbs'] = [
    "news.tvbs.com.tw",
    "04784784225885481651/3528912055494430107",
    "UC5nwNW4KdC0SzrhF9BXEYOQ"
]
source['ctitv'] = [
    "gotv.ctitv.com.tw",
    "04784784225885481651/5391259535330418203",
    "UCpu3bemTQwAU8PqM4kJdoEQ"
]
source['ettoday'] = [
    "www.ettoday.net",
    "04784784225885481651/10236880490079678464",
    "feeds.feedburner.com/ettoday/realtime"
]
source['ebc'] = [
    "news.ebc.net.tw",
    "04784784225885481651/6967504200194224812"
    "UCR3asjvr_WAaxwJYEDV_Bfw"
]

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
    {'tzinfo': "Asia/Taipei", 'format': ["YYYY-MM-DD\ \ HH:mm", "YYYY-MM-DD"]}
]
context['appledaily'] = [
    {'save': "title", 'path': "header > hgroup > h1", 'ind': 0},
    {'save': "summary", 'path': ["#summary", "div.articulum.trans"], 'ind': 0},
    {'save': "_rawtime", 'path': "time", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': ["YYYY年MM月DD日HH:mm", "YYYY年MM月DD日"]}
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
    {'save': "_rawtime", 'path': [
        ".titleBtnBlock > .title-left-area > .date", ".titleBtnBlock > .time"], 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY/MM/DD HH:mm:ss"}
]
context['eranews'] = [
    {'save': "title", 'path': "#LT_1_1", 'ind': 0},
    {'save': "summary", 'path': "#LT_1_3_1", 'ind': 0},
    {'save': "_rawtime", 'soup': 'find_all', 'path': 'text', 'ind': 4},
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
    {'save': "summary", 'path': "p", 'ind': -1},
    {'save': "_rawtime", 'soup': "attrs", 'path': {'time': "datetime"}, 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY-MM-DD"}
]
context['ettoday'] = [
    {'save': "title", 'path': ["h2", "h1.title"], 'ind': 0},
    {'save': "summary", 'path': ["section > p", ".subjcet_article > .story"], 'ind': -1},
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

trimtext['any'] = []
trimtext['ltn'] = ['相關影音']
trimtext['ctitv'] = ['※中天快點TV非讀不可:']
trimtext['udn'] = ['分享facebook']
trimtext['appledaily'] = ['有話要說 投稿「即時論壇」']
