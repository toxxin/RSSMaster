# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2015, Easywhere"
__email__ = "ag@easywhere.ru"

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, UnicodeText, TIMESTAMP, func

DeclarativeBase = declarative_base()


class RSSFeed(DeclarativeBase):
    __tablename__ = 'tr_rss'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    url = Column(u'url', String(255), nullable=False)
    guid = Column(u'guid', String(255), nullable=False)
    link = Column(u'link', String(255), nullable=False)
    title = Column(u'title', UnicodeText, nullable=False)
    desc = Column(u'desc', UnicodeText, nullable=True)
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    published = Column(u'published', TIMESTAMP(), nullable=False)
    pic = Column(u'pic', String(255), nullable=True)

    def __init__(self, url, guid, link, title, desc, published, pic=None):
        self.url = url
        self.guid = guid
        self.link = link
        self.title = title
        self.desc = desc
        self.published = published
        self.pic = pic