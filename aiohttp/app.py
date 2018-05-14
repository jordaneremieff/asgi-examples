from aiohttp import web
from aiohttp.http import RawRequestMessage
from yarl import URL


class AioHttpAsgiAdapter:

    def __init__(self, app):
        self.app = app
        self.request = None

    def __call__(self, scope):
        aio_message = RawRequestMessage(
            method=scope['method'],
            path=scope['path'],
            version=scope['http_version'],
            headers=dict(scope['headers']),
            raw_headers=dict(scope['headers']),
            should_close=False,
            compression=False,
            upgrade=False,
            chunked=False,
            url=URL(scope['path'])
        )
        #self.request = 

        async def asgi_instance(receive, send):
            request = self.app._make_request(aio_message, None, 'http', None, None)
            response = await self.app._handle(request)
            body = response.body
            if not isinstance(body, bytes):
                body = body.encode()
            headers = [(k.encode(), v.encode()) for k, v in response.headers.items()]
            await send({
                'type': 'http.response.start',
                'status': response.status,
                'headers': headers,
            })
            await send({
                'type': 'http.response.body',
                'body': body,
                'more_body': False,
            })

        return asgi_instance


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


webapp = web.Application()
webapp.add_routes([web.get('/', handle),
                   web.get('/{name}', handle)])

app = AioHttpAsgiAdapter(webapp)

# TODO: Websocket

# async def wshandle(request):
#     ws = web.WebSocketResponse()
#     await ws.prepare(request)

#     async for msg in ws:
#         if msg.type == web.WSMsgType.text:
#             await ws.send_str("Hello, {}".format(msg.data))
#         elif msg.type == web.WSMsgType.binary:
#             await ws.send_bytes(msg.data)
#         elif msg.type == web.WSMsgType.close:
#             break

#     return ws
