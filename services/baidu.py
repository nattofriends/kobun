#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

from pyquery import PyQuery as pq
import requests

import gevent
import urllib

handshake("glorious chinese search engine")

config = load_config()


def worker(server, target, query):
    try:
        p = pq(url="http://www.baidu.com/s?wd={}".format(urllib.quote_plus(query)))
    except Exception as e:
        result = "uh, no, that doesn't exist... ({})".format(e)
    else:
        first = p(p(".result .f a")[0])

        if not first:
            result = "(no result)"

        result = u"{}: {}".format(first.text(), first.attr("href"))

    write_line(server, "PRIVMSG", [target, "\x02Glorious China:\x02 {}".format(result.encode("utf-8"))])

def core():
    while True:
        server, prefix, command, args = read_line()

        if command.lower() == "privmsg":
            target, msg = args

            parts = msg.split(" ", 1)
            if parts[0].lower() == "!baidu":
                query = parts[1:] and parts[1] or ""
                gevent.spawn(worker, server, target, query)

        gevent.sleep(0)

gevent.spawn(core).join()
