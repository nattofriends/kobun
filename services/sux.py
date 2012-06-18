#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

handshake("you hit wtc")

config = load_config()


while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        parts = msg.split(" ", 1)

        if len(parts) != 2:
            continue

        if parts[0].lower() == "!sux":
            write_line(server, "PRIVMSG", [target, "fuck {what}; {what} sucks; {what} is dying; {what} is dead to me; {what} hit wtc".format(what=parts[1].strip())])

