class AsgiAdapter:

    def __init__(self, app):
        self.app = app
        self.protocol_router = {"http": {}, "websocket": {}}

    def __call__(self, scope):
        protocol = scope["type"]
        path = scope["path"]
        try:
            consumer = self.protocol_router[protocol][path]
        except KeyError:
            consumer = None
        if consumer is not None:
            return consumer(scope)
        return self.build_response(scope)

    def build_response(self, scope, *args, **kwargs):
        raise NotImplementedError

    def send_response(self, scope, body=b"", more_body=False, status=200, headers=[]):

        async def asgi_instance(receive, send):
            await send(
                {"type": "http.response.start", "status": status, "headers": headers}
            )
            await send(
                {"type": "http.response.body", "body": body, "more_body": more_body}
            )

        return asgi_instance

    def asgi(self, rule, *args, **kwargs):
        try:
            protocol = kwargs["protocol"]
        except KeyError:
            raise Exception("You must define a protocol type for an ASGI handler")

        def _route(func):
            self.protocol_router[protocol][rule] = func

        return _route


class AsgiWsgiAdapter(AsgiAdapter):

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

        status = int(wsgi_status.split()[0])
        headers = [
            [k.lower().encode("latin-1"), v.encode("latin-1")] for k, v in wsgi_headers
        ]
        body = b"".join(response)
        return self.send_response(scope, body=body, status=status, headers=headers)
