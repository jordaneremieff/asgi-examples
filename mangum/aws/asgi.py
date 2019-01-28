from mangum.platforms.aws.adapter import AWSLambdaAdapter

# Uncomment an example to use with the adapter

# -- Bocadillo -- #

# import bocadillo

# app = bocadillo.API()


# @app.route("/")
# async def index(req, res):
#     res.text = "Hello, world!"


# -- Starlette -- #

# from starlette.applications import Starlette
# from starlette.responses import PlainTextResponse


# app = Starlette(debug=True)


# @app.route("/")
# def homepage(request):
#     return PlainTextResponse("hello world!")

# -- Quart -- #

# from quart import Quart

# app = Quart(__name__)


# @app.route("/")
# async def hello():
#     return "hello world!"


handler = AWSLambdaAdapter(app)
