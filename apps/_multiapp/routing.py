# Django Channels

from channels.routing import ProtocolTypeRouter

# afiqah

from afiqah import Afiqah
from afiqah.consumers import HttpResponse

# aiohttp

from aiohttp import web
from aiohttp.http import RawRequestMessage
from yarl import URL

# Flask

from flask import Flask

# from ._aiohttp import AioHttpAsgiAdapter


class AioHttpAsgiAdapter:

    def __init__(self, app):
        self.app = app
        self.request = None

    def __call__(self, scope):
        aio_message = RawRequestMessage(
            method=scope["method"],
            path=scope["path"],
            version=scope["http_version"],
            headers=dict(scope["headers"]),
            raw_headers=dict(scope["headers"]),
            should_close=False,
            compression=False,
            upgrade=False,
            chunked=False,
            url=URL(scope["path"]),
        )

        async def asgi_instance(receive, send):
            request = self.app._make_request(aio_message, None, "http", None, None)
            response = await self.app._handle(request)
            body = response.body
            if not isinstance(body, bytes):
                body = body.encode()
            headers = [(k.encode(), v.encode()) for k, v in response.headers.items()]
            await send(
                {
                    "type": "http.response.start",
                    "status": response.status,
                    "headers": headers,
                }
            )
            await send({"type": "http.response.body", "body": body, "more_body": False})

        return asgi_instance


class FlaskAsgiAdapter:

    def __init__(self, wsgi):
        self.wsgi = wsgi
        self.route = wsgi.route

    def __call__(self, scope):
        environ = {
            "REQUEST_METHOD": scope.get("method", "GET"),
            "SCRIPT_NAME": scope.get("root_path", ""),
            "PATH_INFO": scope["path"],
            "QUERY_STRING": scope["query_string"].decode("latin-1"),
            "SERVER_PROTOCOL": "http/%s" % scope.get("http_version", "0.0"),
            "wsgi.url_scheme": scope.get("scheme", "http"),
        }
        if "server" in scope:
            environ["SERVER_NAME"] = scope["server"][0]
            environ["SERVER_PORT"] = str(scope["server"][1])
        else:
            environ["REMOTE_ADDR"] = scope["client"][0]
            environ["REMOTE_PORT"] = str(scope["client"][1])
        headers = dict(scope["headers"])
        if b"content-type" in headers:
            environ["CONTENT_TYPE"] = headers.pop(b"content-type")
        if b"content-length" in headers:
            environ["CONTENT_LENGTH"] = headers.pop(b"content-length")
        for key, val in headers.items():
            key_str = "HTTP_%s" % key.decode("latin-1").replace("-", "_").upper()
            val_str = val.decode("latin-1")
            environ[key_str] = val_str

        wsgi_status = None
        wsgi_headers = None

        def start_response(status, headers, exc_info=None):
            nonlocal wsgi_status, wsgi_headers
            wsgi_status = status
            wsgi_headers = headers

        response = self.wsgi(environ, start_response)

        status = int(wsgi_status.split()[0])
        headers = [
            [k.lower().encode("latin-1"), v.encode("latin-1")] for k, v in wsgi_headers
        ]
        body = b"".join(response)

        async def asgi_instance(receive, send):
            await send(
                {"type": "http.response.start", "status": status, "headers": headers}
            )
            await send({"type": "http.response.body", "body": body, "more_body": False})

        return asgi_instance


async def aiohttp_handler(request):
    text = "Hello from aiohttp!"
    return web.Response(text=text)


aiohttp_app = web.Application()
aiohttp_app.add_routes(
    [web.get("/", aiohttp_handler), web.get("/{name}", aiohttp_handler)]
)


flask_app = Flask(__name__)


@flask_app.route("/flask")
def flask_handler():
    return "Hello from Flask!"


afiqah_app = Afiqah(debug=True)


@afiqah_app.route("/flask")
def flask_adapter(scope):

    return FlaskAsgiAdapter(flask_app)(scope)


@afiqah_app.route("/aiohttp")
def aiohttp_adapter(scope):
    return AioHttpAsgiAdapter(aiohttp_app)(scope)


@afiqah_app.route("/afiqah")
def afiqah(scope):
    return HttpResponse(scope, body=b"Hello from Afiqah!")


application = ProtocolTypeRouter({"http": afiqah_app})
