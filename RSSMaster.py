# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__version__ = "0.1.1"
__copyright__ = "Copyright 2015, Easywhere"
__email__ = "ag@easywhere.ru"

import logging
import ConfigParser

from RSSGen import RSSGen

links = [
    'http://auto.vesti.ru/export/auto.vesti.rss',
    'http://www.topgearrussia.ru/10148/rss/d870a12e.xml',
    'http://motor.ru/export/atom/',
    'http://old.avtomir.com/rss/rss.xml',
    'http://carsguru.net/rss/news/'
]

config = ConfigParser.ConfigParser()
config.read('config.ini')

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == '__main__':

    for url in links:
        log.debug("URL in processing: %s", url)
        gen = RSSGen(url)
        try:
            ret = gen.generate()
            for r in ret:
                log.debug("guid: %s", r['guid'])
                log.debug("link: %s", r['link'])
                log.debug("title: %s", r['title'])
                log.debug("desc: %s", r['desc'])
                log.debug("published: %s", r['published'])
                # log.debug("pic: %s", r['pic'])
        except:
            log.debug("Cannot generate data.")