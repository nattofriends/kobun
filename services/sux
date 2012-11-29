#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

import inflect

handshake("you hit wtc")

config = load_config()

p = inflect.engine()


while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        parts = msg.split(" ", 1)

        if len(parts) != 2:
            continue

        if parts[0].lower() == "!sux":
            what = parts[1].strip()
            if not p.singular_noun(what):
                write_line(server, "PRIVMSG", [target, "fuck {what}; {what} sucks; {what} is dying; {what} is dead to me; {what} hit wtc".format(what=what)])
            else:
                write_line(server, "PRIVMSG", [target, "fuck {what}; {what} suck; {what} are dying; {what} are dead to me; {what} hit wtc".format(what=what)])
