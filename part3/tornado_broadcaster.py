from logging import getLogger

import tornado
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
logger = getLogger(__name__)


class Broadcaster(WebSocketHandler):
    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        Broadcaster.clients.append(self)

    def on_close(self):
        Broadcaster.clients.remove(self)

    def on_message(self, message):
        Broadcaster.broadcast_message(message)

    @classmethod
    def broadcast_message(cls, message):
        print("Sharing ", message, "to ", cls.clients)
        for client in cls.clients:
            try:
                client.write_message(message)
            except:
                logger.error("Failed posting broadcast message", exc_info=True)


def main():
    app = tornado.web.Application([
        (r"/", Broadcaster),
    ])
    app.listen(8001)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
