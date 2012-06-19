#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line
import sys
import os

handshake("secret pipe backdoor")

config = load_config()

try:
    os.unlink("pipedoor")
except OSError:
    pass


os.mkfifo("pipedoor")

f = open("pipedoor", "w")

while True:
    sys.stdout.write(f.readline())
