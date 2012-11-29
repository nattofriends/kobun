#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

import requests

import gevent
import urllib
import json

import HTMLParser

import sys

handshake("western barbarian search engine")

config = load_config()

html_parser = HTMLParser.HTMLParser()


def worker(server, target, query):
    try:
        req = requests.get("https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q={}".format(urllib.quote_plus(query)))
    except Exception as e:
        result = "Exception: {}".format(e)
    else:
        results = json.loads(req.text).get("responseData", {}).get("results", [])

        if not results:
            result = "(no result)"

        result = u"{}: {}".format(
            html_parser.unescape(results[0]["titleNoFormatting"]),
            urllib.unquote(results[0]["url"])
         )

    write_line(server, "PRIVMSG", [target, "\x02Google:\x02 {}".format(result.encode("utf-8"))])

def core():
    while True:
        server, prefix, command, args = read_line()

        if command.lower() == "privmsg":
            target, msg = args

            parts = msg.split(" ", 1)
            if parts[0].lower() == "!g":
                query = parts[1:] and parts[1] or ""
                gevent.spawn(worker, server, target, query)

        gevent.sleep(0)

gevent.spawn(core).join()
