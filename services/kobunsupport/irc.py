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

