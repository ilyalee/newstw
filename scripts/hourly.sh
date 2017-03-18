#!/bin/bash

include_text="消防"
timeout=420
url="http://localhost:9530/api/v1/archive"
#url="http://52.198.78.110/news_archiver/api/v1/archive"
http --ignore-stdin --timeout=$timeout POST $url include=$include_text url='http://news.ltn.com.tw/rss/focus.xml'
http --ignore-stdin --timeout=$timeout POST $url include=$include_text url='http://www.appledaily.com.tw/rss/create/kind/rnews/type/new'
http --ignore-stdin --timeout=$timeout POST $url include=$include_text url='http://www.chinatimes.com/rss/realtimenews.xml'
http --ignore-stdin --timeout=$timeout POST $url include=$include_text url='https://udn.com/rssfeed/news/1'
http --ignore-stdin --timeout=$timeout POST $url include=$include_text url='https://www.google.com.tw/alerts/feeds/04784784225885481651/1432933957568832221'
