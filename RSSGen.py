# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2015, Easywhere"
__email__ = "ag@easywhere.ru"

import calendar as cal
import feedparser
import logging


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
        self._url = url

    def _html_escape(self, text):
        """Produce entities within text."""
        return "".join(self._html_escape_table.get(c,c) for c in text)

    def _make_date(self, tmp):
        """Timestamp is output format."""
        if tmp.get('published_parsed') is not None:
            return cal.timegm(tmp['published_parsed'])
        elif tmp.get('updated_parsed') is not None:
            return cal.timegm(tmp['updated_parsed'])
        else:
            logging.debug("Unknown datetime field or format!")
            return 0

    def _get_link(self, links):
        """Attempt to grab images from feed."""
        if links:
            imgs = [l['href'] for l in links if l['type'] == u'image/jpeg']
            return imgs[-1] if imgs else None
        else:
            return None

    def _fillFeed(self, entry):

        return {
            "guid": entry['id'],
            "link": entry['link'],
            "title": entry['title'],
            "desc": entry['summary'] if entry['summary'] else None,
            "published": self._make_date(entry),
            "pic": self._get_link(entry['links'])
        }

    def generate(self):
        feed = feedparser.parse(self._url)
        return [self._fillFeed(e) for e in feed['entries']]