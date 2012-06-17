#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line
from kobunsupport.irc import parse_prefix

import os
import re

from cobe.brain import Brain

handshake("kobun's wonderful brain")

config = load_config()

if not os.path.exists("brain.db"):
    Brain.init("brain.db", tokenizer="MegaHAL")
brain = Brain("brain.db")

while True:
    server, prefix, command, args = read_line()
    nickname = config["servers"][server]["nick"]

    if command.lower() == "privmsg":
        nick, user, host = parse_prefix(prefix)
        target, msg = args

        if re.compile(re.escape(nickname), re.IGNORECASE).search(msg):
            if re.compile(r"^{}[:,]?".format(re.escape(nickname)), re.IGNORECASE).match(msg):
                msg = re.compile(r"^{}[:,]? ".format(re.escape(nickname)), re.IGNORECASE).sub("", msg)
                reply = brain.reply(msg).encode("utf-8")
                write_line(server, "PRIVMSG", [target, "{}: {}".format(nick, reply)])
            else:
                reply = brain.reply(msg).encode("utf-8")
                write_line(server, "PRIVMSG", [target, reply])

        brain.learn(msg)

