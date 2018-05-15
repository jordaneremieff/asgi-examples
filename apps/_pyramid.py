from .utils.adapter import AsgiWsgiAdapter

from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response("Hello %(name)s!" % request.matchdict)


with Configurator() as config:
    config.add_route("hello", "/hello/{name}")
    config.add_view(hello_world, route_name="hello")
    app = AsgiWsgiAdapter(config.make_wsgi_app())
