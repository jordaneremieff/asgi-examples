from .utils.adapter import AsgiAdapter
from .utils.consumers import HttpResponse

from aiohttp import web
from aiohttp.http import RawRequestMessage
from yarl import URL


class AioHttpAsgiAdapter(AsgiAdapter):
    """An example AIOHTTP->ASGI adapter"""

    def build_response(self, scope):
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
        request = self.app._make_request(aio_message, None, "http", None, None)

        async def asgi_instance(receive, send):

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


async def hello(request):
    name = request.match_info.get("name", "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


webapp = web.Application()
app = AioHttpAsgiAdapter(webapp)


@app.asgi("/asgi", protocol="http")
def hello_http(scope):
    text = "Hello, asgi."
    return HttpResponse(scope, body=text)


webapp.add_routes([web.get("/", hello), web.get("/{name}", hello)])


# TODO: Websocket
