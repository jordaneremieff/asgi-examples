# https://github.com/almarklein/asgish

import asgish

@asgish.to_asgi
async def app(request):
   return "<html>hello world</html>"
