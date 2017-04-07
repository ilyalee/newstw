#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fbfeed.utils.fbfeed_utils import load_fb_source
from utils.pprint_helper import pprint_color

import unittest


class TestFBFeedUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_load_fb_source(self):
        name = load_fb_source("")
        self.assertEqual(name, "any")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
