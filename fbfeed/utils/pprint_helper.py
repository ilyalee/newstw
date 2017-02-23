#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from pprint import pformat
import json


def pprint_color(obj, indent=2):
    print(highlight(json.dumps(obj, sort_keys=True, indent=indent,
                               ensure_ascii=False), JsonLexer(), TerminalFormatter()))
