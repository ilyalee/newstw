#!/usr/bin/env python
# -*- coding: utf-8 -*-


def load_lang(lang, value):
    import configparser
    config = configparser.ConfigParser()
    config.read(f'config/lang/{lang}.cfg')
    try:
        ret = config.get('zh_tw', value)
    except configparser.NoOptionError:
        pass
    else:
        return ret
