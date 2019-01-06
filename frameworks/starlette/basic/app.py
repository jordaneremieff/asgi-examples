from starlette.applications import Starlette
from starlette.responses import PlainTextResponse


app = Starlette(debug=True)


@app.route("/")
def homepage(request):
    return PlainTextResponse("hello world!")
