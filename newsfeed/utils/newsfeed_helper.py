#!/usr/bin/env python
# -*- coding: utf-8 -*-

def flag(t):
    return str(t).lower() in ("yes", "true", "t", "1")


def load_remote_news_date(published_list):
    import arrow
    collect = []
    for published in published_list:
        time = arrow.get(published).time()
        if time.minute != 0 and time.second != 0:
            collect.append(published)
        else:
            collect.append("")
    return collect
