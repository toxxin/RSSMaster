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

    def _html_escape(self, text):
        """Produce entities within text."""
        return "".join(self._html_escape_table.get(c,c) for c in text)

    def _make_date(self, tmp):
        """Make timestamp, clean timezone on debug PC"""
        if tmp.get('published') is not None:
            date = tmp['published'][:-5] + "+0000"
            date = datetime.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S +0000")
            return date
        elif tmp.get('updated_parsed') is not None:
            return cal.timegm(tmp['updated_parsed'])
        else:
            print "test"

    def _get_link(self, links):

        if len(links) > 0:
            imgs = [l for l in links if l['type'] == u'image/jpeg']
            return imgs[0]['href'] if len(imgs) > 0 else None
        else:
            return None

    def _fillFeed(self, entry):

        return {
            "guid": entry['id'],
            "link": entry['link'],
            "title": entry['title'],
            "desc": entry['summary'],
            "published": self._make_date(entry),
            # "published": self._make_date(entry['published']) if entry['published'] is not None else self._make_date(entry['updated']),
            # "pic": self._get_link(entry['links'])
        }

    def generate(self):
        feed = feedparser.parse(self._url)
        return [self._fillFeed(e) for e in feed['entries']]