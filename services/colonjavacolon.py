#!/usr/bin/env python2
# encoding: utf-8

from kobunsupport import load_config, handshake, read_line, write_line

import random

handshake(":java:")

config = load_config()

PREFIXES =  [
    "",
    "Abstract",
    "Basic",
    "Virtual",
    "Intermediate",
    "Advanced",
    "Composite",
]

BODIES = [
    "Request",
    "Delegate",
    "Filter",
    "Chain",
    "Context",
    "Proxy",
    "Handler",
    "Listener",
    "Observer",
    "Visitor",
    "Client",
    "Command",
    "Mediator",
    "Interpreter",
]

SUFFIXES = [
    "",
    "Impl",
    "Factory",
    "Adaptor",
    "Decorator",
    "Memento",
    "Bridge",
    "Builder",
    "Singleton",
    "State",
    "Strategy",
    "Multiton",
    "Prototype",
    "Controller",
    "Wrapper",
    "Facade",
    "Specification",
    "Monitor",
    "Reactor",
    "Proactor",
]

while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        if ":java:" in msg:
            write_line(server, "PRIVMSG", [target, random.choice(PREFIXES) + "".join(random.choice(BODIES) for _ in xrange(random.randint(3, 5))) + random.choice(SUFFIXES)])

