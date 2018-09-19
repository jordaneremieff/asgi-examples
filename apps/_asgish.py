# https://github.com/almarklein/asgish

from asgish import handler2asgi

@handler2asgi
async def app(request):
   return "<html>hello world</html>"
