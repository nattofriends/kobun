import shlex
import re
import uuid
import os
import sys
import json

import gevent
import gevent.pool

from . import irc
from gevent import subprocess

import functools
import logging

log = logging.getLogger("kobun.hypervisor")


class ServiceError(Exception): pass


class HypervisedService(object):
    def __init__(self, hypervisor, fn):
        self.hypervisor = hypervisor
        self.fn = fn
        self.greenlet = None

        try:
            self.proc = subprocess.Popen([os.path.join("services", fn), self.hypervisor.config_fn],
                                         stdout=subprocess.PIPE,
                                         stdin=subprocess.PIPE)
        except OSError as e:
            raise ServiceError(str(e))

    def handshake(self):
        k = uuid.uuid4().hex

        self.proc.stdin.write(k + "\n")
        self.proc.stdin.flush()

        try:
            gevent.socket.wait_read(self.proc.stdout.fileno())
        except gevent.socket.timeout:
            self.proc.kill()
            raise ServiceError("did not handshake in time")

        l, info = self.proc.stdout.readline().strip().split(" ", 1)

        if k != l:
            self.proc.kill()
            raise ServiceError("did not handshake in correctly")

        log.info("Handshaked {}: {}".format(self.fn, info))

    def monitor(self):
        self.greenlet = gevent.getcurrent()

        while True:
            gevent.socket.wait_read(self.proc.stdout.fileno())
            server, raw_line = self.proc.stdout.readline().split(" ", 1)
            self.proc.stdout.flush()
            self.hypervisor.irc_clients[server].raw(raw_line[:1000])

    def start(self):
        g = gevent.spawn(self.handshake)
        g.link(lambda _: self.monitor())
        return g

    def stop(self):
        gevent.kill(self.greenlet)

        try:
            self.proc.kill()
        except OSError as e:
            pass


class Hypervisor(object):
    RC_EXPR = re.compile("!hypervisor(?: (?P<params>.*))?")

    def __init__(self, config_fn):
        self.config_fn = config_fn
        self.load_config(config_fn)

        self.irc_clients = {}
        self.irc_group = gevent.pool.Group()

        self.service_clients = {}

    def register_service(self, service):
        self.service_clients[service.fn] = service

    def load_service(self, fn):
        if fn in self.service_clients:
            raise ServiceError("Service already loaded")
        service = HypervisedService(self, fn)
        g = service.start()
        g.link(lambda _: self.register_service(service))
        return service, g

    def unload_service(self, fn):
        if fn not in self.service_clients:
            raise ServiceError("Service not loaded")
        self.service_clients[fn].stop()
        del self.service_clients[fn]

    def load_config(self, fn):
        with open(fn, "r") as f:
            self.config = json.load(f)

    def start_services(self):
        greenlets = []

        for client_fn in self.config["services"]:
            try:
                service, g = self.load_service(client_fn)
            except ServiceError as e:
                log.warn("Could not load {}: {}".format(client_fn, e))
            else:
                greenlets.append(g)

        gevent.joinall(greenlets)

    def start_irc(self):
        for server, details in self.config["servers"].iteritems():
            hn, sport = server.rsplit(":", 2)
            irc_client = irc.IRCClient((hn, int(sport)),
                                       details["nick"],
                                       details["user"],
                                       details["realname"],
                                       source_address=details.get("source_address"))
            irc_client.on_raw = functools.partial(self.on_raw, server)
            irc_client.on_privmsg = functools.partial(self.on_privmsg, irc_client)
            self.irc_clients[server] = irc_client

        for irc_client in self.irc_clients.values():
            self.irc_group.add(gevent.spawn(irc_client._main))

    def run(self):
        log.info("Starting service clients...")
        self.start_services()

        log.info("Starting IRC clients...")
        self.start_irc()

        self.irc_group.join()

    def notify_error(self, e):
        log.warn("Hypervisor Error: {}".format(e))

    def on_raw(self, server, line):
        for client_fn, service in self.service_clients.items():
            try:
                service.proc.stdin.write(server.encode("utf-8") + " " + line + "\n")
                service.proc.stdin.flush()
            except OSError as e:
                self.notify_error("{} died: {}".format(client_fn, e))
                self.unload_service(service.fn)
                self.load_service(service.fn)

    def on_privmsg(self, irc_client, prefix, target, message):
        if not any(re.match(admin_expr, prefix) for admin_expr in self.config["servers"][irc_client.server]["admins"]):
            return

        if target[0] != '#':
            target = prefix.split('!', 2)[0]

        match = self.RC_EXPR.match(message)

        if match:
            params = match.group("params")

            if params:
                if params.split(" ", 1)[0].lower() == "eval": # special case for eval!
                    try:
                        c = params.split(" ", 1)[1:]
                        result = eval(c[0] if c else "")
                    except BaseException as e:
                        irc_client.send_msg(
                            target,
                            "\x02Failed evaluation:\x02 {}: {}".format(
                                e.__class__.__name__,
                                e
                            )
                        )
                    else:
                        irc_client.send_msg(
                            target,
                            "\x02Evaluation result:\x02 {}".format(repr(result))
                        )
                else:
                    params = shlex.split(params)

                    if params[0].lower() == "services":
                        params = params[1:]

                        if params:
                            if params[0] == "load":
                                if len(params) != 2:
                                    irc_client.send_msg(
                                        target,
                                        "\x02Hypervisor Error:\x02 need 1 parameter exactly"
                                    )
                                else:
                                    service = params[1]
                                    try:
                                        self.load_service(service)
                                    except ServiceError as e:
                                        irc_client.send_msg(
                                            target,
                                            "\x02Service Error for {}:\x02 {}".format(service, e)
                                        )
                                    else:
                                        irc_client.send_msg(
                                            target,
                                            "\x02Loaded:\x02 {}".format(service)
                                        )
                            elif params[0] == "unload":
                                if len(params) != 2:
                                    irc_client.send_msg(
                                        target,
                                        "\x02Hypervisor Error:\x02 need 1 parameter exactly"
                                    )
                                else:
                                    service = params[1]
                                    try:
                                        self.unload_service(service)
                                    except ServiceError as e:
                                        irc_client.send_msg(
                                            target,
                                            "\x02Service Error for {}:\x02 {}".format(service, e)
                                        )
                                    else:
                                        irc_client.send_msg(
                                            target,
                                            "\x02Unloaded:\x02 {}".format(service)
                                        )

                            elif params[0] == "reload":
                                if len(params) != 2:
                                    irc_client.send_msg(
                                        target,
                                        "\x02Hypervisor Error:\x02 need 1 parameter exactly"
                                    )
                                else:
                                    service = params[1]
                                    try:
                                        self.unload_service(service)
                                    except ServiceError as e:
                                        irc_client.send_msg(
                                            target,
                                            "\x02Service Error for {}:\x02 {}".format(service, e)
                                        )
                                    else:
                                        irc_client.send_msg(
                                            target,
                                            "\x02Unloaded:\x02 {}".format(service)
                                        )
                                    try:
                                        self.load_service(service)
                                    except ServiceError as e:
                                        irc_client.send_msg(
                                            target,
                                            "\x02Service Error for {}:\x02 {}".format(service, e)
                                        )
                                    else:
                                        irc_client.send_msg(
                                            target,
                                            "\x02Loaded:\x02 {}".format(service)
                                        )

                        else:
                            irc_client.send_msg(
                                target,
                                "\x02{} service(s) under hypervisor:\x02 {}".format(
                                    len(self.service_clients),
                                    ", ".join(sorted(self.service_clients))
                                )
                            )
                    elif params[0].lower() == "irc":
                        params = params[1:]

                        if params:
                            pass
                        else:
                            irc_client.send_msg(
                                target,
                                "\x02{} IRC connection(s) under hypervisor:\x02 {}".format(
                                    len(self.irc_clients),
                                    ", ".join(sorted(self.irc_clients))
                                )
                            )

                    elif params[0].lower() == "reboot":
                        for irc_client in self.irc_clients.values():
                            irc_client.send_command("QUIT", "Reboot requested")

                        for service in self.service_clients.values():
                            service.stop()

                        os.execvp(os.path.join(sys.path[0], sys.argv[0]), sys.argv)
                    elif params[0].lower() == "reload":
                        self.load_config(self.config_fn)
                        irc_client.send_msg(
                            target,
                            "Reloaded configuration, requesting all service clients to reboot."
                        )

                        for service in self.service_clients.keys():
                            self.unload_service(service)
                            self.load_service(service)

                        irc_client.send_msg(
                            target,
                            "Reload complete."
                        )
            else:
                irc_client.send_msg(
                    target,
                    "\x02Hypervisor summary:\x02 {} service client(s), {} IRC client(s)".format(
                        len(self.service_clients),
                        len(self.irc_clients)
                    )
                )

