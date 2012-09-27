#!/usr/bin/env python2
# encoding: utf-8

from kobunsupport import load_config, handshake, read_line, write_line

import binascii
import time

handshake("probably")

config = load_config()

while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        parts = msg.split(" ", 1)

        if len(parts) != 2:
            continue

        if parts[0].lower() == "!decide":
            options = sorted(parts[1].split(' or '), key=lambda x: x.lower())
            write_line(server, "PRIVMSG", [target, "\x02I say:\x02 {}".format(
                options[(binascii.crc32(" or ".join(options).lower()) + int(time.time() // (60 * 60 * 24))) % len(options)]
            )])

