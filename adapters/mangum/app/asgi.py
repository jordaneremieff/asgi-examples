from mangum import Mangum

# import bocadillo
from fastapi import FastAPI

# from starlette.applications import Starlette
# from starlette.responses import PlainTextResponse
# from quart import Quart


# -- Raw ASGI example -- #


# def app(scope):
#     async def asgi(receive, send):
#         await send(
#             {
#                 "type": "http.response.start",
#                 "status": 200,
#                 "headers": [[b"content-type", b"text/plain"]],
#             }
#         )
#         await send({"type": "http.response.body", "body": b"Hello, world!"})

#     return asgi


# -- FastAPI -- #
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# -- Bocadillo -- #

# app = bocadillo.API()


# @app.route("/asgi/bocadillo/hello")
# async def index(req, res):
#     res.text = "Hello, world!"


# -- Starlette -- #

# app = Starlette()


# @app.route("/hello")
# def homepage(request):
#     return PlainTextResponse("hello world!")


# -- Quart -- #
# app = Quart(__name__)


# @app.route("/hello")
# async def hello():
#     return "hello world!"


handler = Mangum(app, debug=True)


# handler = Mangum(App)
