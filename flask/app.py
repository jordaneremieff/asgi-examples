from flask import Flask, render_template


class HttpConsumer:

    def __init__(self, scope, body=b'', status=200, headers=[[b'content-type', b'text/plain']]):
        self.scope = scope
        if not isinstance(body, bytes):
            body = body.encode()
        self.body = body
        self.status = status
        self.headers = headers

    async def __call__(self, receive, send):
        await send({
            'type': 'http.response.start',
            'status': self.status,
            'headers': self.headers,
        })
        await send({
            'type': 'http.response.body',
            'body': self.body,
            'more_body': False,
        })


class WebSocketConsumer:

    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        while True:
            message = await receive()
            if message['type'] == 'websocket.connect':
                response = {
                    'type': 'websocket.accept'
                }
                await send(response)
            if message['type'] == 'websocket.receive':
                response = {
                    'type': 'websocket.send',
                }
                if 'text' in message:
                    response['text'] = message['text']
                else:
                    response['bytes'] = message['bytes']
                await send(response)
            if message['type'] == 'websocket.disconnect':
                return


class AsgiAdapter:

    def __init__(self, wsgi, *args, **kwargs):
        self.wsgi = wsgi
        self.route = wsgi.route
        self.protocol_router = {
            'http': {},
            'websocket': {},
        }

    def __call__(self, scope):
        environ = {
            'REQUEST_METHOD': scope['method'],
            'SCRIPT_NAME': scope.get('root_path', ''),
            'PATH_INFO': scope['path'],
            'QUERY_STRING': scope['query_string'].decode('latin-1'),
            'SERVER_PROTOCOL': 'http/%s' % scope['http_version'],
            'wsgi.url_scheme': scope.get('scheme', 'http'),
        }
        if scope.get('client'):
            environ['REMOTE_ADDR'] = scope['client'][0]
            environ['REMOTE_PORT'] = str(scope['client'][1])
        if scope.get('server'):
            environ['SERVER_NAME'] = scope['server'][0]
            environ['SERVER_PORT'] = str(scope['server'][1])
        headers = dict(scope['headers'])
        if b'content-type' in headers:
            environ['CONTENT_TYPE'] = headers.pop(b'content-type')
        if b'content-length' in headers:
            environ['CONTENT_LENGTH'] = headers.pop(b'content-length')
        for key, val in headers.items():
            key_str = 'HTTP_%s' % key.decode('latin-1').replace('-', '_').upper()
            val_str = val.decode('latin-1')
            environ[key_str] = val_str

        protocol = scope['type']
        path = scope['path']

        try:
            consumer = self.protocol_router[protocol][path]
        except KeyError:
            consumer = None

        if consumer is not None:
            return consumer(scope)

        wsgi_status = None
        wsgi_headers = None

        def start_response(status, headers, exc_info=None):
            nonlocal wsgi_status, wsgi_headers
            wsgi_status = status
            wsgi_headers = headers

        response = self.wsgi(environ, start_response)

        status = int(wsgi_status.split()[0])
        headers = [
            [key.lower().encode('latin-1'), val.encode('latin-1')]
            for key, val in wsgi_headers
        ]
        body = b''.join(response)
        return HttpConsumer(scope, body=body, status=status, headers=headers)

    def asgi(self, rule, *args, **kwargs):
        protocol = kwargs.pop('protocol')

        def _route(func):
            self.protocol_router[protocol][rule] = func
        return _route


app = AsgiAdapter(Flask(__name__))


@app.route("/")
def hello():
    return render_template('hello.html')


@app.asgi("/asgi", protocol="http")
def hello_asgi(scope):
    return HttpConsumer(scope, body="Hello ASGI!", status=200)


@app.asgi("/ws", protocol="websocket")
def hello_websocket(scope):
    return WebSocketConsumer(scope)
