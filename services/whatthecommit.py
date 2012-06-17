#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

import gevent
import requests

handshake("whatthecommit")

config = load_config()


def worker(server, target):
    write_line(server, "PRIVMSG", [target, "\x02WhatTheCommit:\x02 {}".format(requests.get("http://whatthecommit.com/index.txt").text.strip().replace("\n", " "))])

def core():
    while True:
        server, prefix, command, args = read_line()

        if command.lower() == "privmsg":
            target, msg = args

            if msg.strip().lower() == "!wtc":
                gevent.spawn(worker, server, target)

        gevent.sleep(0)

gevent.spawn(core).join()

