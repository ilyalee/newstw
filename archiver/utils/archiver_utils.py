#!/usr/bin/env python
# -*- coding: utf-8 -*-


def load_sources_by_category(category):
    import configparser
    config = configparser.ConfigParser()
    config.read('config/feeds.cfg')
    sources_pm, _ = zip(*config.items("Print media"))
    sources_em, _ = zip(*config.items("Electronic media"))
    sources = []
    if category == 'pmedia':
        sources = sources_pm
    elif category == 'emedia':
        sources = sources_em
    elif category in sources_pm or category in sources_em:
        sources = [category]
    return sources
