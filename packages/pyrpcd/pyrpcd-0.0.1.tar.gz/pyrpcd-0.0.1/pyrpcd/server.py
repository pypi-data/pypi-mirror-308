import argparse
import asyncio
import importlib
import inspect
import multiprocessing
import os
import pathlib
import re
import signal
import sys
import threading
import traceback

import voxe
import tornado
import tornado.websocket
from .share import managers


running_state = True


def sig_handler(sig, frame):
    global running_state
    running_state = False
    print("> Recycle done! exiting ...")
    exit(0)


signal.signal(signal.SIGINT, sig_handler)


def self_import(pth: str):
    if (os.path.isdir(pth) and os.path.isfile(os.path.join(pth, '__init__.py'))) \
            or os.path.isfile(pth + '.py'):
        return importlib.import_module(pth)


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--prefix', type=str, default='/')
    parser.add_argument('--static_path', type=str, default='www')
    parser.add_argument('--cache_path', type=str, default='cache')
    parser.add_argument('module')
    return parser.parse_args(args)


def encode_filename(s: str) -> str:
    return "".join(['%02X' % e for e in s.encode('utf-8')])


def decode_filename(s: str) -> str:
    return b''.join([bytes.fromhex(s[i * 2:i * 2 + 2]) for i in range(len(s) // 2)]).decode('utf-8')


def save_partition(filename: str, section: str, data: bytes, cache_path: str):
    cache_path = pathlib.Path(cache_path)
    if not cache_path.exists():
        cache_path.mkdir()
    encoded_filename = encode_filename(f"{section}:{filename}")
    with open(cache_path / encoded_filename, "wb") as fp:
        fp.write(data)
    filesize = int(section.split(':')[0])
    indexes, size = {}, 0
    for pth in cache_path.iterdir():
        if pth.is_file() and re.match(r"^[A-Fa-f0-9]+$", pth.name):
            decoded_filename = decode_filename(pth.name)
            if f":{filename}" not in decoded_filename:
                continue
            items = str(decoded_filename).split(':')
            _, start, end, name = int(items[0]), int(items[1]), int(items[2]), items[3]
            if start not in indexes:
                indexes[start] = (start, end, pth)
                size += end - start
    if size != filesize:
        return
    print("  merging :", filename)
    with open(cache_path / f"{filename}", 'wb') as fp:
        sections = [indexes.get(k) for k in indexes]
        sections.sort(key=lambda x: x[0])
        for _section in sections:
            pth = _section[2]
            with open(pth, 'rb') as ep:
                fp.write(ep.read())
            os.remove(pth)


class RemoteManager:
    def __del__(self):
        del managers[self]

    def __init__(self):
        managers.add(self)
        self.connections = set()
        self.subscribers = []
        self.queue = asyncio.Queue()
        self.loop = asyncio.new_event_loop()

    async def queue_loop(self):
        global running_state
        while running_state:
            try:
                item = await asyncio.wait_for(self.queue.get(), timeout=0.25)
                for ws in self.connections:
                    try:
                        await ws.write_message(item)
                    except Exception as e:
                        print(str(e))
                self.queue.task_done()
            except asyncio.QueueEmpty:
                pass
            except asyncio.TimeoutError:
                pass

    def launch_queue(self):
        def th():
            self.loop.run_until_complete(self.queue_loop())

        threading.Thread(target=th).start()

    def launch_server(self, module, port=8080, prefix='/', static_path='www', cache_path='cache'):
        root = os.getcwd()
        sys.path.append(root)
        scope = self_import(module)
        print('load scope :', module)
        print('---')
        print(' ', '\n  '.join([e for e in dir(scope) if not re.match(r"__[a-zA-Z0-9]*__", e)]))
        print('---')
        if prefix == '':
            prefix = '/'
        if not prefix.endswith('/'):
            prefix += '/'
        if not prefix.startswith('/'):
            prefix = '/' + prefix
        tornado.web.Application([
            (f'{prefix}websocket', WebsocketMessageHandler, dict(scope=scope, remote=self)),
            (f'{prefix}upload', PartitionUploadHandler, dict(cache_path=cache_path)),
            (f'{prefix}rpc/([_a-zA-Z][_a-zA-Z0-9]*?)$', RPCHandler, dict(scope=scope, remote=self)),
            (r'^/(.*?)$', tornado.web.StaticFileHandler, {"path": static_path, "default_filename": "index.html"},),
        ]).listen(port)
        print("listening on port {}".format(port))
        tornado.ioloop.IOLoop.current().start()

    def publish(self, message):
        async def _pub(x):
            await self.queue.put(x)

        asyncio.run_coroutine_threadsafe(_pub(message), self.loop)


class WebsocketMessageHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, scope, remote):
        self.scope = scope
        self.remote = remote

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self, *args: str, **kwargs: str):
        self.remote.connections.add(self)
        print("websocket open :", self.request.remote_ip)


    def on_close(self):
        self.remote.connections.remove(self)
        print("websocket close :", self.request.remote_ip)

    def on_message(self, message):
        for subscribe in self.remote.subscribers:
            try:
                subscribe(message)
            except Exception as e:
                traceback.print_exception(e)


class PartitionUploadHandler(tornado.web.RequestHandler):
    def initialize(self, cache_path):
        self.cache_path = cache_path

    def post(self):
        section = self.request.headers.get('Section')
        filename = self.request.headers.get('Filename')
        save_partition(filename, section, self.request.body, self.cache_path)
        self.write(dict(success=True, code=200))


class RPCHandler(tornado.web.RequestHandler):
    def initialize(self, scope, remote):
        self.scope = scope
        self.remote = remote

    def post(self, *args, **kwargs):
        method_name = self.request.uri.split('/')[-1]
        try:
            args = voxe.loads(self.request.body)
        except Exception as e:
            print(self.request.body)
            traceback.print_exception(e)
            self.write(str(e))
            return
        print("rpc method :", method_name, ", args :", args if args is not None else '')
        args = list(voxe.loads(self.request.body)) if len(self.request.body) > 0 else []
        try:
            method = self.scope.__getattribute__(method_name)
        except Exception as e:
            print(f'No such method {method_name}!')
            traceback.print_exception(e)
            self.write(voxe.dumps(Exception(f'No such method {method_name}!')))
            return
        try:
            resp = method(*args) if callable(method) else method
            # print("execute success, response :", resp)
        except Exception as e:
            resp = e
        self.write(voxe.dumps(resp))


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    remote = RemoteManager()
    remote.launch_queue()
    remote.launch_server(args.module, args.port, args.prefix, args.static_path, args.cache_path)
