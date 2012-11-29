#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

import datetime

handshake("legacy-style kobun logger")

config = load_config()

f = open(config["logger.file"], "a", 0)

while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        f.write("{} [KobunClient,client] {} <{}> {}\n".format(
            datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S+0000"), target, prefix, msg
        ))

