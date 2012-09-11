import gevent
from gevent import socket

import logging
log = logging.getLogger("kobun.irc")

def parse_line(s):
    """
    Shamelessly stolen from Twisted.
    """
    prefix = ''
    trailing = []
    if not s:
       raise ValueError("s")
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing.rstrip("\r"))
    else:
        args = s.split()
    command = args.pop(0)
    return prefix, command, args

def make_line(command, args):
    """
    Create a message.
    """
    if len(args) > 1:
        args_raw = " ".join(args[:-1]) + " :{}".format(args[-1])
    else:
        args_raw = ":{}".format(args[0])
    return "{} {}".format(command, args_raw)

def parse_prefix(prefix):
    nick, rest = prefix.split("!", 1)
    user, host = rest.split("@", 1)
    return nick, user, host

CONTROL_CODES = {
    "B": "\x02", # bold
    "U": "\x1f", # underline
    "O": "\x0f", # reset
    "K": "\x03"  # color
}

class IRCClient(object):
    def __init__(self, address, nick, user, realname, source_address=None):
        self.address = address
        self.gsock = socket.create_connection(address, source_address=(source_address, 0))

        self.nick = nick
        self.user = user
        self.realname = realname

    @property
    def server(self):
        return "{}:{}".format(*self.address)

    def main(self):
        buf = ""

        self.send_command("NICK", self.nick)
        self.send_command("USER", self.user, "*", "*", self.realname)

        log.info("Established connection to {}:{}".format(*self.address))

        while True:
            buf += self.gsock.recv(8195)
            lines_raw, buf = buf.rsplit("\n", 1)
            lines = lines_raw.split("\n")

            for line in lines:
                self.on_raw(line)
                self.process_comamnd(parse_line(line))

            gevent.sleep(0)

    def process_comamnd(self, line):
        log.debug("< {}".format(line))
        prefix, command, args = line

        getattr(self, "on_{}".format(command.lower()), lambda *args: None)(prefix, *args)

    def send_command(self, command, *args):
        line_raw = make_line(command, args)
        log.debug("> {}".format((command, args)))
        self.raw(line_raw)

    def send_msg(self, target, msg):
        self.send_command("PRIVMSG", target, msg)

    def on_raw(self, line):
        pass

    def raw(self, line):
        self.gsock.send(line + "\n")

    def on_ping(self, *args):
        self.send_command("PONG", args)

    def run(self):
        gevent.spawn(self.main).join()

