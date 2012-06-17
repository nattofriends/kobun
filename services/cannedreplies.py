#!/usr/bin/env python2
# encoding: utf-8

from kobunsupport import load_config, handshake, read_line, write_line

import random

handshake("erryday i'm gfacing")

config = load_config()


RESPONSES = {
    "gface":    u"( ≖‿≖)",
    "cool":     u"COOL LIKE SNOWMAN ☃"
}

while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        cands = []
        for cand, repl in RESPONSES.iteritems():
            if cand in msg:
                cands.append(repl)

        if cands:
            write_line(server, "PRIVMSG", [target, random.choice(cands).encode("utf-8")])

