from nardis.asgi import main
from nardis.routing import Get as get


async def hello(req, res):
    await res.send("Hello world!")


routes = [get(r"^/?$", hello)]
config = {"routes": routes}
app = main(config)
