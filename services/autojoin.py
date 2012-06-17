#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

handshake("auto-join to channels")

config = load_config()

while True:
    server, prefix, command, args = read_line()

    if command == "376":
        for channel in config["servers"][server]["channels"]:
            write_line(server, "JOIN", [channel])

