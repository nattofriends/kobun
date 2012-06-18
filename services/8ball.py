#!/usr/bin/env python2
# encoding: utf-8

from kobunsupport import load_config, handshake, read_line, write_line

import binascii
import time

handshake("probably")

config = load_config()

OPTIONS = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes, definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy, try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"
]

while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        parts = msg.split(" ", 1)

        if len(parts) != 2:
            return

        if parts[0].lower() == "!8ball":
            write_line(server, "PRIVMSG", [target, "\x02The Magic 8-Ball says:\x02 {}".format(
                OPTIONS[(len(binascii.crc32(parts[1]) + int(time.time() // (60 * 60 * 24))) % options)]
            )])

