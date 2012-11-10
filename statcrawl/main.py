# -*- coding: utf-8 -*-

import requests as rq
from lxml.html import fromstring

from statcrawl import conf

ROOT = u"http://makstat.stat.gov.mk/pxweb2007bazi/Database/Статистика%20по%20области"
JS_INDEX = u"/databasetreeNodes.js"

ENC = 'cp1251' # encoding of pages


def main():
    """Get all stat pages with lookup in javascript tree index"""
    js_index = rq.get(ROOT + JS_INDEX).content.decode(ENC)
    subpages = set()
    for line in js_index.split(u"Статистика по области"):
        if '"' not in line: continue
        line = line.split('"')[0]
        subpages.add(ROOT + line)

    map(crawl_subpage, subpages)


def crawl_subpage(link):
    """Crawl every stat page and download 
       all .px data files in path specified in conf"""
    base = '/'.join(link.split('/')[:-1]) + '/'
    content = rq.get(link).content

    try:
        content = content.decode(ENC)
    except UnicodeDecodeError:
        print 'decode error:', link
        return

    doc = fromstring(content)
    for link in doc.cssselect("a[href]"):
        name = link.attrib['href']
        if name.lower().endswith('.px'):
            href = base + name
            px_content = rq.get(href).content
            with open(conf.datapath + '/' + name, 'w') as f:
                f.write(px_content)


if __name__ == '__main__':
    main()
