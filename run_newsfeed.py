#!/usr/bin/env python
# -*- coding: utf-8 -*-

import better_exceptions
from newsfeed import newsfeed
import os

debug = __debug__
host = "0.0.0.0"
port = 9528

newsfeed.app.run(host=host, port=port, debug=debug, workers=os.cpu_count())
