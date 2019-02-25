from lemon.app import Lemon
from lemon.context import Context


async def handle(ctx: Context):
    ctx.body = {"msg": "hello world"}


app = Lemon(debug=True)

app.use(handle)

app.listen()
