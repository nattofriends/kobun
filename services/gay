#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

handshake("www.hahgay.com")

config = load_config()

COLORS = [
    4, 5, 8, 9, 10, 12, 13, 6
]

while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        parts = msg.split(" ", 1)

        if len(parts) != 2:
            continue

        if parts[0].lower() == "!gay":
            what = parts[1].strip().decode("utf-8")
            buf = ""

            for i, x in enumerate(what):
                buf += "\x03{:02}{}".format(COLORS[i % len(COLORS)], x.encode("utf-8"))

            write_line(server, "PRIVMSG", [target, buf])

