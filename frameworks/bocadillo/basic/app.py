import bocadillo

app = bocadillo.API()


@app.route("/")
async def index(req, res):
    res.text = "Hello, world!"
