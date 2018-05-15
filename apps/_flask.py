from .utils.adapter import AsgiAdapter
from .utils.consumers import HttpResponse

from flask import Flask, render_template


class FlaskAsgiAdapter(AsgiAdapter):
    """An example WSGI->ASGI adapter tailored towards Flask"""

    def build_response(self, scope, *args, **kwargs):
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

        response = self.app(environ, start_response)

        # Handle the WSGI response to be return by our ASGI callable

        status = int(wsgi_status.split()[0])
        headers = [
            [k.lower().encode("latin-1"), v.encode("latin-1")] for k, v in wsgi_headers
        ]
        body = b"".join(response)
        return self.send_response(scope, body=body, status=status, headers=headers)

    def route(self, *args, **kwargs):
        return self.app.route(*args, **kwargs)


app = FlaskAsgiAdapter(Flask(__name__))


@app.route("/")
def hello():
    return render_template("hello.html")


@app.asgi("/asgi", protocol="http")
def hello_http(scope):
    return HttpResponse(scope, body="Hello from asgi.")


@app.asgi("/ws", protocol="websocket")
def hello_websocket(scope):

    async def asgi_instance(receive, send):
        while True:
            message = await receive()
            if message["type"] == "websocket.connect":
                response = {"type": "websocket.accept"}
                await send(response)
            if message["type"] == "websocket.receive":
                response = {"type": "websocket.send"}
                if "text" in message:
                    response["text"] = message["text"]
                else:
                    response["bytes"] = message["bytes"]
                await send(response)
            if message["type"] == "websocket.disconnect":
                return

    return asgi_instance
