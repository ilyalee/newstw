#!/usr/bin/env python
# -*- coding: utf-8 -*-

import facebook
import settings
from urllib.parse import urlparse, parse_qs
from itertools import islice


def fb_init():
    return facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN, version=settings.FACEBOOK_API_VERSION)

'''
ref:  https://github.com/mobolic/facebook-sdk/issues/85
      https://github.com/mobolic/facebook-sdk/pull/298
'''


def get_all_connections(graph, fbid, connection, **args):
    while True:
        page = graph.get_connections(fbid, connection, **args)
        for post in page['data']:
            yield post
        next = page.get('paging', {}).get('next')
        if not next:
            return
        args = parse_qs(urlparse(next).query)
        del args['access_token']


def load_obj(graph, fbid, **args):
    try:
        obj = graph.get_object(fbid, **args)
        return obj
    except facebook.GraphAPIError as e:
        if __debug__:
            print(e)
        return None


def load_pages(graph, fbid, connection, num=1, **args):
    gen = get_all_connections(graph, fbid, connection, **args)
    collect = list(islice(gen, 0, num))
    return collect
