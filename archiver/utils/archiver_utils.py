#!/usr/bin/env python
# -*- coding: utf-8 -*-


def load_sources_by_category(category):
    import configparser
    config = configparser.ConfigParser()
    config.read('config/feeds.cfg')
    sources_pm, _ = zip(*config.items("Print media"))
    sources_em, _ = zip(*config.items("Electronic media"))
    sources_cat = lambda category: [category] if category in set(
        sources_pm) or category in set(sources_em) else []
    return {'pmedia': sources_pm, 'emedia': sources_em}.get(category, sources_cat(category))
