#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Divers auteurs'
SITENAME = "Python I/O"
SITETITLE = "Python I/O"
SITESUBTITLE = "Articles et news par des Pythonistas passionnés"
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/favicon-32x32.png': {'path': 'favicon-32x32.png'}}
FAVICON = 'favicon-32x32.png'
MAIN_MENU = True
DISPLAY_PAGES_ON_MENU = False
MENUITEMS = [
    ('News', '/category/news.html'),
    ('Articles', '/category/articles.html'),
    ('Tutoriels', '/category/tutoriels.html'),
    ('Catégories', '/categories.html'),
    ('Tags', '/tags.html'),
]

TIMEZONE = 'Europe/Paris'

# Translate to German.
DEFAULT_LANG = 'fr'

DEFAULT_CATEGORY = 'Autres'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

PYGMENTS_RST_OPTIONS = {'linenos': 'inline'}

THEME = './themes/white_cloud'
PYGMENTS_RST_OPTIONS = {'classprefix': 'pgcss', 'linenos': 'table'}
