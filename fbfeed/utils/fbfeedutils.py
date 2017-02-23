#!/usr/bin/env python
# -*- coding: utf-8 -*-

import facebook
import settings
from urllib.parse import urlparse, parse_qs

def FBInit():
    return facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN, version=settings.FACEBOOK_API_VERSION)

'''
ref:  https://github.com/mobolic/facebook-sdk/issues/85
      https://github.com/mobolic/facebook-sdk/pull/298
'''
def getAllConnections(graph, fbid, connection, **args):
    while True:
        page = graph.get_connections(fbid, connection, **args)
        for post in page['data']:
            yield post
        next = page.get('paging', {}).get('next')
        if not next:
            return
        args = parse_qs(urlparse(next).query)
        del args['access_token']

def loadGroup(graph, fbid, **args):
    try:
        group = graph.get_object(fbid, **args)
        return group
    except facebook.GraphAPIError as err:
        if __debug__:
            print(err)
        return None

def loadPages(graph, fbid, connection, num=1, **args):
    collect = []
    gen = getAllConnections(graph, fbid, connection, **args)
    for i in range(num):
        collect.append(next(gen))
    return collect
