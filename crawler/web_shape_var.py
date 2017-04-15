#!/usr/bin/env python
# -*- coding: utf-8 -*-

context = {}
skip = {}
source = {}
trimtext = {}

source_default = 'any'
source['chinatimes'] = [
    "chinatimes.com",
    "04784784225885481651/11191251640937190187"
]
source['ltn'] = [
    "ltn.com.tw",
    "04784784225885481651/6747397391254853783"
]
source['appledaily'] = [
    "www.appledaily.com.tw",
    "04784784225885481651/11191251640937192952"
]
source['udn'] = [
    "udn.com",
    "04784784225885481651/11191251640937192594"
]
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
    "ettoday.net",
    "04784784225885481651/10236880490079678464",
    "feeds.feedburner.com/ettoday/realtime"
]
source['ebc'] = [
    "news.ebc.net.tw",
    "04784784225885481651/6967504200194224812"
    "UCR3asjvr_WAaxwJYEDV_Bfw"
]
source['supplements'] = [
    "04784784225885481651/13939194059460916207",
    "04784784225885481651/17213960256688867711",
    "04784784225885481651/6443552349257533219",
    "04784784225885481651/6443552349257535467",
    "04784784225885481651/3004179234881120660",
    "04784784225885481651/3004179234881119137"
]
source['youtube'] = [
    "youtube.com",
    "youtu.be"
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
    {'save': "title", 'path': [".caption > h2", ".container > h2", "h1"], 'ind': 0},
    {'save': "summary", 'path': ["#newstext", ".news_content",
                                 ".wordright", "article > .boxTitle"], 'ind': -1},
    {'save': "_rawtime", 'path': ["#newstext > span",
                                  ".news_content > .date", ".time", ".label-date", "h1 > span"], 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': ["YYYY-MM-DD\ \ HH:mm",
                                         "YYYY/MM/DD HH:mm", "YYYY-MM-DD", "MMM. DD YYYY"]}
]
context['appledaily'] = [
    {'save': "title", 'path': "header > hgroup > h1", 'ind': 0},
    {'save': "summary", 'path': ["#summary", "div.articulum.trans"], 'ind': 0},
    {'save': "_rawtime", 'path': "time", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': ["YYYY年MM月DD日HH:mm", "YYYY年MM月DD日"]}
]
context['udn'] = [
    {'save': "title", 'path': ["#story_body_content > h1", "#story_art_title"], 'ind': 0},
    {'save': "summary", 'path': "p", 'ind': -1},
    {'save': "_rawtime", 'path': [".story_bady_info_author", "time"], 'ind': 0},
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
    {'save': "_rawtime", 'path': [".news-time", ".date"], 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': ["YYYY年MM月DD日 HH:mm", "時間： YYYY/MM/DD HH:mm"]}
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
trimtext['appledaily'] = [
    '有話要說 投稿「即時論壇」',
    '想了解更多中部房市訊息，請到蘋果地產王粉絲團',
    '【加入環境資訊中心粉絲頁，掌握環境新知！】',
    '【更多新聞，請看《蘋果陪審團》粉絲團】'
]
