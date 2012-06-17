#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line
from kobunsupport.irc import parse_prefix

from stemming.lovins import stem

handshake("quotemania")

config = load_config()

import re
import sqlite3

conn = sqlite3.connect("quotes.db")
conn.execute("""CREATE TABLE IF NOT EXISTS quotes(
    id INTEGER PRIMARY KEY,
    quote TEXT,
    context VARCHAR(255)
)""")

COMMAND_EXPR = re.compile("!quote (?P<command>add|del|rand|view|read|find)(?: (?P<args>.*))?")

def insert_quote(quote, context):
    cur = conn.cursor()
    cur.execute("INSERT INTO quotes(quote, context) VALUES(?, ?)", (quote, context))
    conn.commit()
    return cur.lastrowid

def random_quote(context=None):
    cur = conn.cursor()
    if context is not None:
        cur.execute("SELECT id, quote FROM quotes WHERE context=? ORDER BY RANDOM() LIMIT 1", (context,))
    else:
        cur.execute("SELECT id, quote FROM quotes ORDER BY RANDOM() LIMIT 1")
    return cur.fetchone()

def delete_quote(id, context):
    cur = conn.cursor()
    cur.execute("DELETE FROM quotes WHERE id=? AND context=?", (id, context))
    conn.commit()
    return cur.rowcount != 0

def view_quote(id, context=None):
    cur = conn.cursor()
    if context is not None:
        cur.execute("SELECT id, quote FROM quotes WHERE id=? AND context=?", (id, context))
    else:
        cur.execute("SELECT id, quote FROM quotes WHERE id=?", (id,))
    return cur.fetchone()

def find_quote(like, context=None):
    likes = [
        "%" + stem(l.strip()).replace("!", "!!").replace("%", "!%") + "%"
        for l in like.split(" ")
    ]

    clauses = ["quote LIKE ? ESCAPE \"!\""] * len(likes)
    clause = " AND ".join(clauses)

    cur = conn.cursor()

    if context is not None:
        cur.execute("SELECT id FROM quotes WHERE {0} AND context=?".format(clause), likes + [context])
    else:
        cur.execute("SELECT id FROM quotes WHERE {0}".format(clause), likes)
    return [ row[0] for row in cur.fetchall() ]

while True:
    server, prefix, command, args = read_line()
    nickname = config["servers"][server]["nick"]

    if command.lower() == "privmsg":
        nick, user, host = parse_prefix(prefix)
        target, msg = args

        nick, user, host = parse_prefix(prefix)
        match = COMMAND_EXPR.match(msg)

        if match is not None:
            command = match.group("command")
            args = match.group("args")

            if args:
                args = args.strip()

            if command == "add":
                if not args:
                    write_line(server, "PRIVMSG", [target, "Did you forget to enter a quote?"])
                else:
                    qid = insert_quote(args.decode("utf-8"), target.lower())
                    write_line(server, "PRIVMSG", [target, "Quote {} added.".format(qid)])
            elif command == "del":
                if delete_quote(args, target.lower()):
                    write_line(server, "PRIVMSG", [target, "Quote {} deleted.".format(args)])
                else:
                    write_line(server, "PRIVMSG", [target, "Quote {} not found.".format(args)])
            elif command == "rand":
                quote = random_quote(target.lower())
                if quote is None:
                    write_line(server, "PRIVMSG", [target, "Quote not found."])
                else:
                    qid, content = quote
                    write_line(server, "PRIVMSG", [target, "\x02Quote {}:\x02 {}".format(qid, content.encode("utf-8"))])
            elif command in ("view", "read"):
                quote = view_quote(args, target.lower())
                if quote is None:
                    write_line(server, "PRIVMSG", [target, "Quote {} not found.".format(args)])
                else:
                    qid, content = quote
                    write_line(server, "PRIVMSG", [target, "\x02Quote {}:\x02 {}".format(qid, content.encode("utf-8"))])
            elif command == "find":
                if not args:
                    write_line(server, "PRIVMSG", [target, "Huh?"])
                else:
                    qids = find_quote(args, target.lower())
                    if not qids:
                        write_line(server, "PRIVMSG", [target, "No quotes found matching criteria."])
                    elif len(qids) == 1:
                        qid, content = view_quote(args, target.lower())
                        write_line(server, "PRIVMSG", [target, "\x02Quote {}:\x02 {}".format(qid, content.encode("utf-8"))])
                    else:
                        write_line(server, "PRIVMSG", [target, "\x02Quotes found:\x02 {}".format(", ".join(str(x) for x in qids))])

