#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line
import json
import urllib
import httplib
import traceback

handshake("image me kobun")

config = load_config()

GOOGLE_SAFE_SEARCH = "off"  # active, moderate, off


def image_search(server, target, keywords):
    """
    Searches for an image using google image search API.
    """
    try:
        conn = httplib.HTTPConnection("ajax.googleapis.com")
        conn.request("GET", "/ajax/services/search/images?safe=%s&v=1.0&q=%s"
                    % (GOOGLE_SAFE_SEARCH, urllib.quote(" ".join(keywords))))
        r1 = conn.getresponse()

        content = r1.read()
        j = json.loads(content)

        url = j['responseData']['results'][0]['unescapedUrl']

        write_line(server, "PRIVMSG", [target, "\x02Google Images:\x02 " + unicode(url)])
    except IndexError as e:
        write_line(server, "PRIVMSG", [target, "\x02Google Images:\x02 (no result)"])

while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        parts = msg.split(" ", 1)

        if len(parts) < 2:
            continue

        if parts[0].lower() == "!image":
            image_search(server, target, parts[1:])
