import responder

app = responder.API()


@app.route("/")
async def hello(req, resp):
    resp.text = "hello world!"
