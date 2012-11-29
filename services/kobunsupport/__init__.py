import sys
import json

from . import irc

def load_config():
    with open(sys.argv[1], "r") as f:
        return json.load(f)

def handshake(info):
    sys.stdout.write("{} {}\n".format(sys.stdin.readline().strip(), info))
    sys.stdout.flush()

def read_line():
    server, raw_line = sys.stdin.readline().rstrip("\r\n").split(" ", 1)
    prefix, command, args = irc.parse_line(raw_line)
    return server, prefix, command, args

def write_line(server, command, args):
    sys.stdout.write(server + " " + irc.make_line(command, args) + "\n")
    sys.stdout.flush()

def parse_prefix(prefix):
    nick, rest = prefix.split("!", 1)
    user, host = rest.split("@", 1)
    return nick, user, host

