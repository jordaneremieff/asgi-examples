# This example is based on the project's documentation :)
# https://pgjones.gitlab.io/quart/asgi_deployments.html

from quart import Quart
from quart.serving import ASGIServer

app = Quart(__name__)


@app.route("/")
async def hello():
    return "hello"


app = ASGIServer(app)
