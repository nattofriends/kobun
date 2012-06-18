#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

import re
import requests
import urllib2

import gevent

from pyquery import PyQuery as pq

handshake("display the title of a page")

config = load_config()

SCAN_EXPR = re.compile(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+')
DESPACE_EXPR = re.compile(r'\s+')

def worker(server, target, url):
    if not (url.startswith("http:") or url.startswith("https:")):
        url = "http://" + url
    try:
        response = requests.head(url)
    except requests.RequestException as e:
        write_line(server, "PRIVMSG", [target, "\x02Request Error:\x02 {}".format(e)])

    if response.headers["content-type"].split(";")[0] not in ("text/html",):
        write_line(server, "PRIVMSG", [target, "\x02Content Type:\x02 {}".format(response.headers["content-type"])])
    else:
        try:
            r = requests.get(url)
            try: # XXX: DIRTY HORRIBLE BUT WORKING HACK
                p = pq(r.text)
            except ValueError:
                p = pq(r.content)

            title = p("title").text()
            if title:
                title = DESPACE_EXPR.sub(" ", raw_title.encode("utf-8").replace("\n", " "))

            write_line(server, "PRIVMSG", [
                target,
                "\x02Title:\x02 {}".format(title or "(no title)")
            ])
        except urllib2.HTTPError as e:
            write_line(server, "PRIVMSG", [target, "\x02Request Error:\x02 {}".format(e)])


def core():
    while True:
        server, prefix, command, args = read_line()

        if command.lower() == "privmsg":
            target, msg = args
            urls = SCAN_EXPR.findall(msg)

            if urls:
                url = urls[0]
                gevent.spawn(worker, server, target, url)

        gevent.sleep(0)

gevent.spawn(core).join()

