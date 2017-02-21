#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawler.utils.crawlerutils import loadContext, loadSkips, loadTrimtext, detectNewsSource
from crawler.utils.crawlerhelper import fetchNews
from crawler.utils.pprinthelper import pprint_color

import unittest
class TestCrawler(unittest.TestCase):
    def setUp(self):
        url = self.urls = {}
        # 四大報
        url['ltn'] = [None] * 1
        url['ltn'][0] = "http://news.ltn.com.tw/news/life/breakingnews/1979996"

        url['appledaily'] = [None] * 1
        url['appledaily'][0] = "http://www.appledaily.com.tw/realtimenews/article/new/20170219/1059540/"

        url['chinatimes'] = [None] * 1
        url['chinatimes'][0] = "http://www.chinatimes.com/realtimenews/20170219000888-260408"

        url['udn'] = [None] * 1
        url['udn'][0] = "https://udn.com/news/story/7316/2294464"

        # 電視傳媒
        url['pts'] = [None] * 1
        url['pts'][0] = "http://news.pts.org.tw/article/350012"

        url['ftv'] = [None] * 1
        url['ftv'][0] = "http://news.ftv.com.tw/NewsContent.aspx?ntype=class&sno=2017220L01M1"

        url['setn'] = [None] * 2
        url['setn'][0] = "http://www.setn.com/News.aspx?NewsID=226627"
        url['setn'][1] = "http://www.setn.com/E/News.aspx?NewsID=226596"

        url['eranews'] = [None] * 1

        url['eranews'][0] = "http://eranews.eracom.com.tw/files/news/xml/era/n59250.xml"

        url['tvbs'] = [None] * 1
        url['tvbs'][0] = "http://news.tvbs.com.tw/fun/708444"

        url['ctitv'] = [None] * 1
        url['ctitv'][0] = "http://gotv.ctitv.com.tw/2017/02/384052.htm"

    def test_detectNewsSource(self):
        for source, urls in self.urls.items():
            for url in urls:
                self.assertEqual(detectNewsSource(url), source)

    def test_loadContext(self):
        from crawler.web_shape_var import context

        for c, _ in self.urls.items():
            self.assertNotEqual(loadContext(c), {})
            self.assertNotEqual(loadContext(c), context['any'], "(%s)" % c)

    def test_loadSkips(self):
        for c, _ in self.urls.items():
            loadSkips(c)
            self.assertTrue(True)

    def test_fetchNews(self):
        for c, urls in self.urls.items():
            for url in urls:
                news = fetchNews(url)
                self.assertIn("title", news)
                self.assertIn("summary", news)
                self.assertIn("_rawtime", news)
                self.assertIn("pubdate", news)
                self.assertIn("link", news)
                self.assertIn("from", news)
                self.assertTrue(True)
                pprint_color(news)

    def test_shortenUrl(self):
        news = fetchNews("https://goo.gl/6IXNnC")
        pprint_color(news)

        self.assertIn("from", news)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
