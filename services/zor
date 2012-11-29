#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

import random

handshake(":v")

config = load_config()

RANTS_ON = {
    'education': ["<Zor> the root problem of most issues like this one is that universities suck at teaching up to date stuff <Zor> if it can't prepare a student for real work, then you may as well study yourself"],
    'economy': ["<Zor> the economy is going to die sooner or later <Zor> infinite growth can't actually work", "<Zor> \"Economic growth is the most important factor for the nation's well-being.\" <-- this is going by the assumption that economy makes sense at all, which it doesn't"],
    'unconstrained nulls': ["<Zor> and any new, serious language should not have unconstrained null <Zor> unconstrained null is where a specific type category can always have an invalid (null) state <Zor> e.g. in C, the pointer category is always nullable <Zor> the right thing to do is to not have null at all and use option types, or alternatively, introduce a nullable type category by suffixing '?' which allows the null state"],
    'windows 8': ["<Zor> but >>>>>>>>>>>>>>>>>>>>>>>windows 8 <Zor> it's good that they want to make their UI/UX consistent <Zor> but oh god fuck metro <Zor> metro is actually ok on tablets and phones <Zor> but it has no fucking business being on a desktop computer <Zor> there's a reason apple didn't shove iOS into OS X"],
    'society': ["<Zor> I do not want to help society <Zor> society is a dumb term for a social unity that doesn't really exist"],
    'social norms': ["<Zor> \"social norms\" is about <Zor> the most irrational explanation <Zor> I have ever heard <Zor> maybe next to religious norms"],
    'religion': ["<Zor> there is everything wrong with religion when it teaches false information to school kids <Zor> people can believe in whatever superstition they want, but spreading false information to try to disprove science is just low <Zor> the funny thing about believing in the bible is that you're not so much beliving in god as you're beliving in the people who wrote it"],
    'suicide': ["<Zor> most people will interpret a straight out suicide in the middle of everything as attention whoring unless you have a really compelling reason to suicide <Zor> (and if you do, you'd usually have the decency to not inconvenience others) <Zor> just leave a suicide note or something <Zor> then go into $largeForest and suicide or some shit <Zor> police will usually not do a very large scale manhunt for someone who's most likely suicided <Zor> and most certainly not for very long <Zor> I think if you don't appear within a week and you'd left a suicide note behind <Zor> your family probably would realize there's no way you could be alive <Zor> but look at me with my rational thinking"]
}

while True:
    server, prefix, command, args = read_line()

    if command.lower() == "privmsg":
        target, msg = args

        parts = msg.split(' ', 1)

        if parts[0] == '!zor':
            if len(parts) == 1:
                write_line(server, "PRIVMSG", [target, "\x02Zor knows about:\x02 {}".format(", ".join(RANTS_ON))])
                continue

            topic = parts[1].lower().strip()

            if topic not in RANTS_ON:
                write_line(server, "PRIVMSG", [target, "Zor hasn't said anything about {} yet. :V".format(topic)])
            else:
                write_line(server, "PRIVMSG", [target, "\x02Zor on {}:\x02 {}".format(topic, random.choice(RANTS_ON[topic]))])

