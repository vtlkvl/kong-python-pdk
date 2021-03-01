import os
import re
import sys
import time
import traceback
import threading
import msgpack

from .const import PY3K
if PY3K:
    from socketserver import ThreadingMixIn, UnixStreamServer as sUnixStreamServer
else:
    from SocketServer import ThreadingMixIn, UnixStreamServer as sUnixStreamServer

from gevent import socket as gsocket, sleep as gsleep, spawn as gspawn
from gevent.server import StreamServer as gStreamServer

from .exception import PluginServerException

cmdre = re.compile("([a-z])([A-Z])")

DEFAULT_SOCKET_NAME = "python_pluginserver.sock"

def write_response(fd, msgid, response):
    fd.send(msgpack.packb([
        1, # is response
        msgid,
        None,
        response
    ]))

def write_error(fd, msgid, error):
    fd.send(msgpack.packb([
        1, # is response
        msgid,
        error,
        None
    ]))

class Server(object):
    def __init__(self, plugin_server):
        self.ps = plugin_server
        self.logger = plugin_server.logger

    def handle(self, fd, address, *_):
        while True:
            msg = fd.recv(1024)
            if not msg:
                return
            # raw=False: decode to str not bytes
            d = msgpack.unpackb(msg, raw=False)
            _, msgid, method, args = d
            ns, cmd = method.split(".")
            if ns != "plugin":
                write_error(fd, msgid, "RPC for %s is not supported" % ns)
                continue

            cmd_r = cmd[0].lower() + cmdre.sub(lambda m: "%s_%s" % (m.group(1), m.group(2).lower()), cmd[1:])
            try:
                self.logger.debug("rpc: #%d method: %s args: %s" % (msgid, method, args))
                ret = getattr(self.ps, cmd_r)(*args)
                self.logger.debug("rpc: #%d return: %s" % (msgid, ret))
                write_response(fd, msgid, ret)
            except PluginServerException as ex:
                self.logger.debug("rpc: #%d error: %s" % (msgid, str(ex)))
                write_error(fd, msgid, str(ex))
            except Exception as ex:
                self.logger.error("rpc: #%d exception: %s" % (msgid, traceback.format_exc()))
                write_error(fd, msgid, str(ex))

class tUnixStreamServer(ThreadingMixIn, sUnixStreamServer):
    pass

def watchdog(sleep, logger):
    while True:
        if os.getppid() == 1: # parent dead, process adopted by init
            logger.info("Kong exits, terminating...")
            sys.exit()
        sleep(1)

class UnixStreamServer(Server):
    def __init__(self, pluginserver, path, sock_name=DEFAULT_SOCKET_NAME, use_gevent=True):
        Server.__init__(self, pluginserver)
        self.path = os.path.join(path, sock_name)
        self.use_gevent = use_gevent
    
    def serve_forever(self):
        if os.path.exists(self.path):
            os.remove(self.path)

        if self.use_gevent:
            listener = gsocket.socket(gsocket.AF_UNIX, gsocket.SOCK_STREAM)
            listener.bind(self.path)
            listener.listen(1)

            self.logger.info("server (gevent) started at path " + self.path)

            gspawn(watchdog, gsleep, self.logger)

            gStreamServer(listener, self.handle).serve_forever()
        else:
            self.logger.info("server started at path " + self.path)

            t = threading.Thread(
                target=watchdog,
                args=(time.sleep, self.logger, ),
            )
            t.setDaemon(True)
            t.start()
            tUnixStreamServer(self.path, self.handle).serve_forever()
