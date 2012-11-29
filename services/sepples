#!/usr/bin/env python2
# encoding: utf-8

from kobunsupport import load_config, handshake, read_line, write_line

import random

handshake(":c++:")

config = load_config()

BODIES = [
    "typedef typename detail::ref<T>::type detail_ref_t;",
    "return dynamic_cast<T<TTail...>&>(*this);",
    "detail::replace<T, U>(std::forward<T>(x));"
]

WRAPPINGS = [
    "namespace detail {{ {} }}",
    "template<typename T> class allocator {{ {} }}",
    "namespace traits {{ {} }}",
    "const char * foo(const T &t, void(T::*f_t)) const {{ {} }}",
    "template<typename THead, typename TTail...> class linked_allocator<THead, TTail...> {{ {} }}",
    "T move(T&& t, U<T>) {{ {} }}"
]

while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        if ":c++:" in msg:
            output = random.choice(BODIES)

            for i in range(random.randint(5, 10)):
                output = random.choice(WRAPPINGS).format(output)

            write_line(server, "PRIVMSG", [target, output])

