#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line
from kobunsupport.irc import parse_prefix
import logging

handshake("nattofriends is a faggot")

config = load_config()

import re

log = logging.getLogger("regex.matching")

REGEX_EXPR = re.compile(r's(.)(?P<find>.*(?!\1).)\1(?P<replace>.*(?!\1).)\1')
HISTORY = {}

RATE_LIMIT = {}
RATE_LIMIT_TIME = 10

while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        nick, user, host = parse_prefix(prefix)
        target, msg = args

        match = REGEX_EXPR.match(msg)

        if match is not None:
            find = match.group("find")
            replace = match.group("replace")
            
            if nick in HISTORY:
                text = HISTORY[nick]

                new_text = re.sub(find, replace, text)
                if not new_text == text:
                    write_line(server, "PRIVMSG", [target, "{} meant: {}".format(nick, new_text)])
        
        HISTORY[nick] = msg
