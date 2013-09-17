COLORS = [
    4, 5, 8, 9, 10, 12, 13, 6
]

def gay(what):
    buf = ""
    for i, x in enumerate(what):
        if x == ' ':
            buf += x.encode("utf-8")
        else:
            buf += "\x03{:02}{}".format(COLORS[i % len(COLORS)], x.encode("utf-8"))
    return buf
