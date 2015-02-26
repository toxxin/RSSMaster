# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2015, Easywhere"
__email__ = "ag@easywhere.ru"

import datetime
import time
import calendar as cal
import feedparser


class RSSGen(object):

    _url = None
    _since = 0

    _html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }

    def __init__(self, url):
        # log.debug("Init new gen object. URL - %s", url)
        self._url = url