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
