from afiqah import Afiqah
from afiqah.consumers import HttpResponse

body = b"""<!DOCTYPE html>
<html>
<head>
</head>
<body>
<h1>afiqah</h1>
<br>
<div id='messages'></h4>
<script>
    var ws = new WebSocket("ws://127.0.0.1:8000/ws");
    ws.onmessage = function(event) {
        var msg = document.createElement('p');
        var messages = document.getElementById('messages')
        content = event.data;
        msg.innerHTML = content;
        messages.appendChild(msg);
    };
</script>
</body>
</html>
"""

app = Afiqah()


@app.route('/')
def home(scope):
    return HttpResponse(scope, body=body, headers=[[b'content-type', b'text/html']])


@app.route('/ws')
def home_ws(scope):
    async def asgi_instance(receive, send):
        message = await receive()
        if message['type'] == 'websocket.connect':
            await send({'type': 'websocket.accept'})
            await send({'type': 'websocket.send', 'text': "Hello world."})
            await send({'type': 'websocket.close', 'code': 1000})
    return asgi_instance
