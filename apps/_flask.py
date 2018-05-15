from .utils.adapter import AsgiWsgiAdapter
from .utils.consumers import HttpResponse

from flask import Flask, render_template


class FlaskAsgiAdapter(AsgiWsgiAdapter):

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
