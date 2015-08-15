# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from bs4 import BeautifulSoup
from collections import namedtuple
import logging
import requests
import urlparse

logger = logging.getLogger(__name__)

__all__ = [b"SearchResult", b"search"]

SearchResult = namedtuple("SearchResult", ["url", "title"])


def search(query):
    r = requests.get("https://www.google.com/search?oe=utf8&ie=utf8&source=uds&start=0&hl=ru&gws_rd=ssl",
                     params={"q": query.encode("utf-8")})
    for a in BeautifulSoup(r.text).select("h3 a"):
        url = dict(urlparse.parse_qsl(urlparse.urlparse(a["href"]).query))["q"]
        logger.debug("Found URL %s", url)
        yield SearchResult(url, a.text)
