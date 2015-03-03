# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__version__ = "0.1.1"
__copyright__ = "Copyright 2015, Easywhere"
__email__ = "ag@easywhere.ru"

import datetime
import logging
import logging.config
import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from RSSGen import RSSGen
from model import RSSFeed, DeclarativeBase

links = [
    'http://auto.vesti.ru/export/auto.vesti.rss',
    'http://www.topgearrussia.ru/10148/rss/d870a12e.xml',
    'http://motor.ru/export/atom/',
    'http://carsguru.net/rss/news/'
]

config = ConfigParser.ConfigParser()
config.read('config.ini')

log = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini')


engine = create_engine('mysql://' + config.get('Database', 'DBUSER') + ':' + config.get('Database', 'DBPASS') + '@' + config.get('Database', 'DBHOST') + ':3306/' + config.get('Database', 'DBNAME') + '?charset=utf8', echo=True, encoding='utf8')
metadata = DeclarativeBase.metadata
metadata.bind = engine


if __name__ == '__main__':

    for url in links:
        log.debug("URL in processing: %s", url)
        session = Session()
        ts = session.query(RSSFeed.guid).filter(RSSFeed.url == url).all()
        gs = [t[0] for t in ts]

        gen = RSSGen(url)
        try:
            ret = gen.generate()
            for r in ret:
                log.debug("guid: %s", r['guid'])
                log.debug("link: %s", r['link'])
                log.debug("title: %s", r['title'])
                log.debug("desc: %s", r['desc'])
                log.debug("published: %s", r['published'])
                log.debug("pic: %s", r['pic'])

                if r['guid'] not in gs:
                    f = RSSFeed(url=url, guid=r['guid'], link=r['link'], title=r['title'], desc=r['desc'],
                                published=datetime.datetime.fromtimestamp(r['published']), pic=r['pic'])
                    session.add(f)

            session.commit()
        except:
            session.rollback()
            log.debug("Cannot generate data.")
        finally:
            session.close()